from taipy.gui import Gui
from rembg import remove
from PIL import Image
from io import BytesIO
from assets.mui_theme import *


path_upload = ""
path_download = "fixed_img.png"
original_image = None
fixed_image = None
fixed = False


header_md = """
<|part|class_name=header sticky|
<|toggle|theme|>
|>
"""

page = header_md + """
<page|layout|columns=300px 1fr|gap=0|
    <sidebar|part|class_name=sidebar|
# Removing Background from your image

<br/>
Upload and download

<|{path_upload}|file_selector|on_action=fix_image|extensions=.png;.jpg|label=Upload original image|>

<br/>
Download it here

<|{path_download}|file_download|label=Download fixed image|bypass_preview|active={fixed}|>
    |sidebar>

    <container|part|class_name=container|
# Image Background Remover

## Remove background from image

🐶 Try uploading an image to watch the background magically removed. 
Full quality images can be downloaded from the sidebar.
This code is open source and available here on [GitHub](). Special thanks to the [rembg]() library 😁

<br/>

        <images|layout|columns=1 1|
            <col1|part|class_name=card|render={fixed}|
Original Image 📷

<center> <|{original_image}|image|> </center>
            |col1>

            <col2|part|class_name=card|render={fixed}|
Fixed Image 🔧

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
    image = Image.open(state.path_upload)#.rotate(90, expand=True)
    
    fixed_image = remove(image)
    fixed_image.save("fixed_img.png")

    state.original_image = convert_image(image)
    state.fixed_image = convert_image(fixed_image)
    state.fixed = True


gui = Gui(page=page)
gui.run()
