from PIL import Image


def add_profile_pic(pic_upload, username):
    filename = pic_upload.filename
    # mypic.jpg this next function grabs jpg
    extenstion_type = filename.split('.')[-1]
    # Next line saves the image they uploaded by their unique usernames
    storage_filename = str(username)+'.'+extenstion_type

    filepath = 'project\static\student\\' + storage_filename

    output_size = (200, 200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename 