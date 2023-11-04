from pyIDM import download,alreadyNotDownloaded, downloadCompleteRegister
import html

def main(response):
    breakpoint()
    videolink = response.css('#ideoooolink::text').get()
    if videolink is None:
        with open('streamtapenot.txt', 'a+') as fp:
                fp.write(response.url+'\n') 
                # return 
        return 
    videolink = videolink.split('token=')[0] 
    token_string =  response.css('script').re('\&token=([^\'\"]*)\'\)\.substring')[-1] 
    videolink =  html.unescape('https:/'+videolink) + 'token=' +token_string + '&stream=1'
    filename = response.url.split('/')[-1]
    # breakpoint()
    filename =  response.css('.col-12.text-center.video-title>h2::text').get()
    # if not response.meta['filename'] is None:
    #     filename =  response.meta['filename'].replace('-',' ').replace('.html','.mp4')
    if alreadyNotDownloaded('streamtape.jav', filename): 
        download(r'D:\paradise\stuff\new\jav', filename, videolink)
        downloadCompleteRegister('streamtape.jav',filename)
        breakpoint()
    # generic_downloader(videolink,filename,filename,4,r'D:\paradise\stuff\new\jav') 
