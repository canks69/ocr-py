from PIL import Image
import pytesseract

def get_text(file_path_and_name) :
    print(pytesseract.image_to_string(Image.open(file_path_and_name)))
    return pytesseract.image_to_string(Image.open(file_path_and_name))