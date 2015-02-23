__author__ = 'moon'
from DIY_tool import settings


def handle_uploaded_image(i, x, y):
    import StringIO
    from PIL import Image, ImageOps
    import os
    from django.core.files.images import ImageFile
    from django.core.files.uploadedfile import  InMemoryUploadedFile
    import uuid


    IMAGE_TYPE=i.content_type

    #PIL_TYPE use to save disk, FILE_EXTENSTION use to make the path
    print
    if IMAGE_TYPE =='image/jpeg':
         PIL_TYPE = 'image/jpg'
         PIL_SAVE = 'JPEG'
         FILE_EXTENSION = 'jpg'
    elif IMAGE_TYPE=='image/png':
        PIL_TYPE = 'image/png'
        PIL_SAVE = 'PNG'
        FILE_EXTENSION = 'png'


    #read image from InMemoryUploadedFile
    image_str = ""
    for c in i.chunks():
        image_str +=c

    #create PIL image instance
    imagefile = StringIO.StringIO(image_str)
    image = Image.open(imagefile)

    # if not RGB, convert
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    #define file output dimensions
    x = x
    y = y

    # get orginal image ratio
    img_ratio = float(image.size[0])/image.size[1]

    #resize but constrain prorpottions?
    if x==0.0:
        x = y* img_ratio
    elif y==0.0:
        y = x/img_ratio

    #output file ratio
    resize_ratio = float(x)/y
    x = int(x); y = int(y)

    #get output with and height to do the first crotp

    if(img_ratio > resize_ratio):
        output_width = x*image.size[1]/y
        output_height = image.size[1]
        originX = image.size[0]/ 2 - output_width /2
        originY = 0
    else :
        output_width = image.size[0]
        output_height = y* image.size[1]/x
        originX = 0
        originY = image.size[1]/ 2 - output_width /2

    #crop
    cropBox = (originX, originY, originX + output_width, originY+output_height)
    image = image.crop(cropBox)

    #resize(doing a thumb)
    image.thumbnail([x,y], Image.ANTIALIAS)

    #re-initialize imageFile and set a hash (unique filename)
    imagefile = StringIO.StringIO()
    filename = str(uuid.uuid1())+"."+FILE_EXTENSION

    #PIL instance(image) change to imagefile
    #return FILE instance after just resize not save
    thumnail_io= StringIO.StringIO()
    image.save(thumnail_io, format=PIL_SAVE)
    thumnail_io.seek(0)

    content = InMemoryUploadedFile(thumnail_io, None, filename, PIL_TYPE,
                                   thumnail_io.len, None)

    """
    #save to disk
    #save first and read again style
    imagefile = open(os.path.join(settings.MEDIA_ROOT, filename), 'w')
    image.save(imagefile, 'JPEG', quality=90)
    image_file = open(os.path.join(settings.MEDIA_ROOT, filename), 'r')
    content = ImageFile(image_file)

    """

    return (filename, content)