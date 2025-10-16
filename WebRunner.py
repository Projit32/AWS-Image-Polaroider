from pyscript import document, window
from pyodide.ffi import create_proxy
from PIL import Image
import io
import base64
from js import console, File, FileReader, Uint8Array
import asyncio

from PolaroidBuilder import generate_polaroid
from PolaroidSettings import ColorMode, PolaroidMode

polaroid_mode_codes = {
    "F": PolaroidMode.FULL_POLAROID,
    "H": PolaroidMode.HALF_POLAROID,
    "Q": PolaroidMode.QUARTER_POLAROID,
    "IS": PolaroidMode.INSTA_SQUARED,
    "FC": PolaroidMode.FULL_POLAROID_COMPACT,
    "HC": PolaroidMode.HALF_POLAROID_COMPACT,
    "QC": PolaroidMode.QUARTER_POLAROID_COMPACT,
    "ISC": PolaroidMode.INSTA_SQUARED_COMPACT,
}

color_mode_code ={
    "D": ColorMode.DARK,
    "L": ColorMode.LIGHT
}


class ImageProcessor:
    def __init__(self):
        self.images = []
        self.proxies = []  # Store proxies to prevent garbage collection
        self.setup_event_listeners()

    def setup_event_listeners(self):
        """Setup all event listeners"""
        image_input = document.getElementById("imageInput")
        submit_btn = document.getElementById("submitBtn")

        # Create proxies for event handlers
        upload_proxy = create_proxy(self.handle_image_upload)
        submit_proxy = create_proxy(self.process_images)

        # Store proxies to prevent garbage collection
        self.proxies.extend([upload_proxy, submit_proxy])

        image_input.addEventListener("change", upload_proxy)
        submit_btn.addEventListener("click", submit_proxy)

    async def handle_image_upload(self, event):
        """Handle image upload and display preview"""
        files = event.target.files
        preview_container = document.getElementById("previewContainer")
        controls = document.getElementById("controls")

        # Clear previous previews and images
        preview_container.innerHTML = ""
        self.images = []

        if files.length == 0:
            preview_container.style.display = "none"
            controls.style.display = "none"
            return

        # Show containers
        preview_container.style.display = "block"
        controls.style.display = "block"

        # Process each file
        for i in range(files.length):
            file = files.item(i)

            # Read file as data URL
            reader = FileReader.new()

            # Create a promise to wait for file reading
            promise = self.read_file_as_data_url(reader, file)
            data_url = await promise

            # Store original image data
            self.images.append({
                'data_url': data_url,
                'name': file.name
            })

            # Create and scale preview image
            img = document.createElement("img")
            img.src = data_url
            img.className = "preview-image"
            img.style.height = "270px"  # 480p height scaled down for preview
            img.style.width = "auto"

            preview_container.appendChild(img)

    async def read_file_as_data_url(self, reader, file):
        """Read file as data URL using promise"""
        future = asyncio.Future()

        def on_load(event):
            future.set_result(reader.result)

        # Create proxy for the callback
        load_proxy = create_proxy(on_load)
        reader.addEventListener("load", load_proxy)
        reader.readAsDataURL(file)

        result = await future
        load_proxy.destroy()  # Clean up the proxy after use
        return result

    async def process_images(self, event):
        """Process all uploaded images"""
        if len(self.images) == 0:
            window.alert("Please upload images first!")
            return

        # Show loading
        loading = document.getElementById("loading")
        loading.style.display = "block"

        # Get selected options
        polaroid_type = document.getElementById("polaroidType").value
        color_type = document.getElementById("color").value

        # Hide controls
        controls = document.getElementById("controls")
        controls.style.display = "none"

        # Process images
        results_grid = document.getElementById("resultsGrid")
        results_container = document.getElementById("resultsContainer")
        results_grid.innerHTML = ""

        await asyncio.sleep(0.1)  # Allow UI to update

        for idx, img_data in enumerate(self.images):
            try:
                # Convert data URL to PIL Image
                pil_image = self.data_url_to_pil(img_data['data_url'])

                color_mode = color_mode_code.get(color_type)
                polaroid_mode = polaroid_mode_codes.get(polaroid_type)

                processed_image = generate_polaroid(pil_image, polaroid_mode, color_mode)
                print("Polaroiding complete")

                # Convert back to data URL
                processed_data_url = self.pil_to_data_url(processed_image)

                # Create result item
                result_item = document.createElement("div")
                result_item.className = "result-item"

                result_img = document.createElement("img")
                result_img.src = processed_data_url
                result_img.style.cursor = "pointer"
                result_img.title = "Click to download"

                # Add click handler for download
                download_proxy = create_proxy(
                    lambda e, url=processed_data_url, name=img_data['name']: self.download_image(url, name, polaroid_mode,
                                                                                                 color_mode))
                result_img.addEventListener("click", download_proxy)

                result_text = document.createElement("p")
                result_text.textContent = f"Image {idx + 1}: {img_data['name']}"

                result_item.appendChild(result_img)
                result_item.appendChild(result_text)
                results_grid.appendChild(result_item)

            except Exception as e:
                console.error(f"Error processing image {idx + 1}: {str(e)}")

        # Hide loading and show results
        loading.style.display = "none"
        results_container.style.display = "block"

    def data_url_to_pil(self, data_url):
        """Convert data URL to PIL Image"""
        # Remove data URL prefix
        header, encoded = data_url.split(',', 1)

        # Decode base64
        image_data = base64.b64decode(encoded)

        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_data))
        return image

    def pil_to_data_url(self, image):
        """Convert PIL Image to data URL"""
        buffer = io.BytesIO()

        image.save(buffer, format="PNG", compress_level=1)

        # Get base64 encoded string
        encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Create data URL
        mime_type = f"image/PNG"
        data_url = f"data:{mime_type};base64,{encoded}"

        return data_url


    def download_image(self, data_url, original_name, polaroid_type, color_type):
        """Download image when clicked"""
        # Create download link
        a = document.createElement("a")
        a.href = data_url

        # Generate filename
        name_without_ext = original_name.rsplit('.', 1)[0] if '.' in original_name else original_name
        a.download = f"{name_without_ext}_{polaroid_type}_{color_type}.png"

        # Trigger download
        a.click()


# Initialize the processor
processor = ImageProcessor()