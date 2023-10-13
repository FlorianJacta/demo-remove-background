from taipy.gui import Gui, notify
from rembg import remove
from PIL import Image
from io import BytesIO


path_upload = ""
path_download = "fixed_img.png"
original_image = None
fixed_image = None
fixed = False


header_md = """
<|toggle|theme|>
"""

page = header_md + """
<page|layout|columns=300px 1fr|
<|sidebar|
### Removing **Background**{: .color-primary} from your image

<br/>
Upload and download

<|{path_upload}|file_selector|on_action=fix_image|extensions=.png;.jpg|label=Upload original image|>

<br/>
Download it here

<|{path_download}|file_download|label=Download fixed image|bypass_preview|active={fixed}|>
|>

    <container|container|part|
# Image Background **Remover**{: .color-primary}

🐶 Try uploading an image to watch the background magically removed. 
Full quality images can be downloaded from the sidebar.
This code is open source and available here on [GitHub](https://github.com/FlorianJacta/demo-remove-background). Special thanks to the [rembg](https://github.com/danielgatis/rembg) library 😁

<br/>

<images|layout|columns=1 1|
            <col1|card text-center|part|render={fixed}|
### Original Image 📷

<center> <|{original_image}|image|> </center>
            |col1>

            <col2|card text-center|part|render={fixed}|
### Fixed Image 🔧

<center> <|{fixed_image}|image|> </center>
            |col2>
        |images>
    |container>
|page>
"""



# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def fix_image(state):
    notify(state, 'info', 'Uploading original image...')
    image = Image.open(state.path_upload)#.rotate(90, expand=True)
    
    notify(state, 'info', 'Removing the background...')
    fixed_image = remove(image)
    fixed_image.save("fixed_img.png")

    notify(state, 'success', 'Background removed successfully!')
    state.original_image = convert_image(image)
    state.fixed_image = convert_image(fixed_image)
    state.fixed = True


gui = Gui(page=page)
gui.run(margin="0px", title='Background Remover')
