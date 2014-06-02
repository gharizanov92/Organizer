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

#def chunks(files, chunk_size):
#    return list(zip(*[iter(files)]*chunk_size))

def get_files():
    all_files = glob.glob("files/*.*")
    all_files = [txt.replace("\\","/") for txt in all_files ]
    all_files = [txt.split('/')[-1] for txt in all_files ]
    return(all_files)