import os
def download(videoPath, filename, videoUrl,forceDownload = False):
    filename = filename
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
    print("videos"+filename[:3])
    if alreadyNotDownloaded("IDMList"+filename[:3], filename) or forceDownload:
        cmd = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
        wholeCommand = 'start "" "%s" /d "%s" /p "%s" /f \"%s\" /n /a "%s"' % (cmd, videoUrl, videoPath, filename,userAgent)
        print(wholeCommand)
        os.system(wholeCommand)
        downloadCompleteRegister("IDMList"+filename[:3], filename)

def alreadyNotDownloaded(fileName, Id):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        fp = open(dir_path + "\\list\\%s.txt" % fileName, "r")
        print("openening file name %s for checking id %s" % (fileName, Id))
    except(FileNotFoundError):
        return True
    data = fp.read()
    fp.close()
    if Id in data:
        print("%s already cntains %s" % (fileName, Id))
        return False
    else:
        return True

def downloadCompleteRegister(fileName, Id,removeLine = False):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Writing file name %s for id %s" % (fileName, Id))
    try:
        line_prepender(dir_path + "\\list\\%s.txt" % fileName, Id)
    except FileNotFoundError as e:
        with open(dir_path + "\\list\\%s.txt" % fileName, 'w') as f:
            line_prepender("list\\%s.txt" % fileName, Id)

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)