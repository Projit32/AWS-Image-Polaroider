import traceback

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
    "Dark": ColorMode.DARK,
    "Light": ColorMode.LIGHT
}

submit_btn = document.getElementById("submitBtn")
results_section = document.getElementById('resultsSection')

class ImageProcessor:
    def __init__(self):
        self.images = []
        self.proxies = []  # Store proxies to prevent garbage collection
        self.setup_event_listeners()

    def setup_event_listeners(self):
        """Setup all event listeners"""
        image_input = document.getElementById("imageUpload")


        # Create proxies for event handlers
        upload_proxy = create_proxy(self.handle_image_upload)
        submit_proxy = create_proxy(self.process_images)

        # Store proxies to prevent garbage collection
        self.proxies.extend([upload_proxy, submit_proxy])

        image_input.addEventListener("change", upload_proxy)
        submit_btn.addEventListener("click", submit_proxy)

        document.getElementById("loadingScreen").classList.add('d-none')
        document.getElementById("polaroidAccordion").classList.remove('d-none')

    async def handle_image_upload(self, event):
        """Handle image upload and display preview"""
        files = event.target.files

        # Clear previous previews and images
        self.images = []

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
        # Add Loading animation
        submit_btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Creating...'
        submit_btn.disabled = True

        """Process all uploaded images"""
        if len(self.images) == 0:
            window.alert("Please upload images first!")
            return

        # Get selected options
        polaroid_type = document.querySelector('input[name="polaroidType"]:checked').value
        color_type = document.getElementById("selectedColor").textContent


        # Process images
        results_container = document.getElementById("resultsContainer")

        await asyncio.sleep(0.1)  # Allow UI to update
        
        # Generate Result Table
        results_container.innerHTML = ''

        for idx, img_data in enumerate(self.images):
            try:
                # Convert data URL to PIL Image
                pil_image = self.data_url_to_pil(img_data['data_url'])

                color_mode = color_mode_code.get(color_type)
                polaroid_mode = polaroid_mode_codes.get(polaroid_type)

                processed_image = generate_polaroid(pil_image, polaroid_mode, color_mode)
                # Convert back to data URL
                processed_data_url = self.pil_to_data_url(processed_image)

                # Generate Card
                resultCard = document.createElement('div')
                resultCard.className = 'result-card'
                resultCard.style.animationDelay = f"{idx * 0.1}s"

                download_proxy = create_proxy(
                    lambda e, url=processed_data_url, name=img_data['name']: self.download_image(url, name,
                                                                                                 polaroid_mode,
                                                                                                 color_mode))

                # Create main image element
                img = document.createElement("img")
                img.src = processed_data_url
                img.alt = f"Polaroid {idx + 1}"
                img.className = "result-card-image"

                # Create result-card-info container
                result_card_info = document.createElement("div")
                result_card_info.className = "result-card-info"

                # Create result-details container
                result_details = document.createElement("div")
                result_details.className = "result-details"

                # Create Name detail item
                name_item = document.createElement("div")
                name_item.className = "result-detail-item"
                name_label = document.createElement("span")
                name_label.className = "result-detail-label"
                name_label.textContent = "Name"
                name_value = document.createElement("span")
                name_value.className = "result-detail-value"
                name_value.textContent = img_data['name']
                name_item.appendChild(name_label)
                name_item.appendChild(name_value)

                # Create Style detail item
                style_item = document.createElement("div")
                style_item.className = "result-detail-item"
                style_label = document.createElement("span")
                style_label.className = "result-detail-label"
                style_label.textContent = "Style"
                style_value = document.createElement("span")
                style_value.className = "result-detail-value"
                style_value.textContent = polaroid_type
                style_item.appendChild(style_label)
                style_item.appendChild(style_value)

                # Create Theme detail item
                theme_item = document.createElement("div")
                theme_item.className = "result-detail-item"
                theme_label = document.createElement("span")
                theme_label.className = "result-detail-label"
                theme_label.textContent = "Theme"
                theme_value = document.createElement("span")
                theme_value.className = "result-detail-value"
                theme_value.textContent = color_type
                theme_item.appendChild(theme_label)
                theme_item.appendChild(theme_value)

                # Append detail items to result-details
                result_details.appendChild(name_item)
                result_details.appendChild(style_item)
                result_details.appendChild(theme_item)

                # Create result-actions container
                result_actions = document.createElement("div")
                result_actions.className = "result-actions"

                # Create download button
                download_btn = document.createElement("button")
                download_btn.className = "btn btn-outline-primary"
                download_btn.title = "Download"
                download_btn.addEventListener("click", download_proxy)

                # Create SVG for download icon
                svg_ns = "http://www.w3.org/2000/svg"
                svg = document.createElementNS(svg_ns, "svg")
                svg.setAttribute("xmlns", svg_ns)
                svg.setAttribute("width", "16")
                svg.setAttribute("height", "16")
                svg.setAttribute("fill", "currentColor")
                svg.setAttribute("class", "bi bi-download")
                svg.setAttribute("viewBox", "0 0 16 16")

                # Create SVG paths
                path1 = document.createElementNS(svg_ns, "path")
                path1.setAttribute("d",
                                   "M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z")

                path2 = document.createElementNS(svg_ns, "path")
                path2.setAttribute("d",
                                   "M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z")

                svg.appendChild(path1)
                svg.appendChild(path2)
                download_btn.appendChild(svg)
                result_actions.appendChild(download_btn)

                # Assemble everything
                result_card_info.appendChild(result_details)
                result_card_info.appendChild(result_actions)

                # Finally, add to parent
                resultCard.appendChild(img)
                resultCard.appendChild(result_card_info)
                results_container.appendChild(resultCard)

            except Exception as e:
                console.error(f"Error processing image {idx + 1}: {str(e)}")
                traceback.print_exc()

        # Show results section
        results_section.classList.remove('d-none')
        results_section.scrollIntoView({ "behavior": 'smooth', "block": 'start' })

        # Reset button
        submit_btn.innerHTML = 'Create Polaroids'
        submit_btn.disabled = False
        results_section.style.animation = 'none'
        def set_transition():
            results_section.style.animation = 'fadeInUp 0.6s ease-out'
        window.setTimeout(set_transition, 10)


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