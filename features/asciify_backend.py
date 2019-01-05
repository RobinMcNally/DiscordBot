import io
import urllib.request
from PIL import Image

ascii_grayscale = [
        '$','@','B','%','8','&','W','M','#','*',
        'o','a','h','k','b','d','p','q','w','m',
        'Z','O','0','Q','L','C','J','U','Y','X',
        'z','c','v','u','n','x','r','j','f','t',
        '/','\\','|','(',')','1','{','}','[',']',
        '?','-','_','+','~','<','>','i','!','l',
        'I',';',':',',','\"','^','`','\'','.',' '
]

def asciify_backend(args):
    if len(args) != 1:
        return "```Expected single argument of type (Url)```"
    try:
        imagedata = io.BytesIO(urllib.request.urlopen(args[0]).read())
        im = Image.open(imagedata)
        #Convert to grayscale
        im = im.convert("L")
    except Exception as err:
        return "```" + err + "```"

