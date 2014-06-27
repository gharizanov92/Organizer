import urllib.request
import glob

def download_from_url(url, block_size=8192, location = ""):
    file_name = "files/" + url.split('/')[-1]
    u = urllib.request.urlopen(url)
    file_stream = open(file_name, 'wb')
    print(u.info()._headers)
    while True:
        buffer = u.read(block_size)
        if not buffer:
            break
        file_stream.write(buffer)
    file_stream.close()

def is_image(file):
    return has_extension(file, ('jpg', 'jpeg', 'png', 'gif'))

def is_doc(file):
    return has_extension(file, ('txt', 'doc', 'docx', 'rtf', 'md'))

def is_archive(file):
    return has_extension(file, ('zip', 'rar', 'iso', 'jar', 'tar', 'gz', '7z','bz2','wim','xz'))

def is_pdf(file):
    return has_extension(file, ('pdf'))

def get_thumbnail(file):
    if is_doc(file):
        return '/images/default_doc.png'

    if is_pdf(file):
        return '/images/pdf.png'

    if is_archive(file):
        return '/images/zipped.png'

    return '/images/default.png'

def has_extension(file, extensions):
    return file.split('.')[-1] in extensions

def get_files():
    all_files = glob.glob("files/*.*")
    all_files = [txt.replace("\\","/") for txt in all_files ]
    all_files = [txt.split('/')[-1] for txt in all_files ]

    result = []

    for file in all_files:

        if is_image(file):
            result.append({'url':'/download/' + file,'is_image':"true"})
        else:
            result.append({'url':'/download/' + file,'thumbnail_url':get_thumbnail(file),'is_image':"false", 'name':file})

    return(result)