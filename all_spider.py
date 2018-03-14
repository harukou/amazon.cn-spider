import requests
import os,re
from bs4 import BeautifulSoup

def get_img_urls(url0): 
    '''获取html并解析出含有jpg资源的tag'''
    try:
        kv={'user-agent':'Mozilla/5.0'}
        r0 = requests.get(url0,headers = kv) #发出请求
        r0.raise_for_status()
        r0.encoding = r0.apparent_encoding
        demo = r0.text                       #获取页面
        html = r0.content
        path0 = r"c:\\test_img\\"+category+r"html\\"
        if not os.path.exists(path0):
            os.makedirs(path0)
        path_html = path0 + url0.split('=')[1] + '.html'
        with open(path_html.replace('?','_'),'wb') as f:
            f.write(html)
    except:
        print('something wrong')
    soup = BeautifulSoup(demo,'lxml')        #解析页面
    global total_url,total_flag
    if total_flag == 0:
        total_url = int(soup.find('span',attrs={'class':'pagnDisabled'}).string) #获取商品页面总数
        print('本商品总页数:',total_url)
        total_flag = 1
    img_urls = []
    for tag in soup.find_all(src=re.compile('.jpg'),class_=re.compile('image')):
        img_urls.append(tag.attrs['src'])    #提取HTML中的图像链接
    return img_urls

def get_pic(img_url,category,img_num,kw):
    path0 = r"c:\\test_img\\"+category+r"\\"                                      
    path = path0+kw+img_url.split('/')[-1]         #建立图像文件名                                          
    try:
        if not os.path.exists(path0):
            os.makedirs(path0)
        if not os.path.exists(path):
            kv={'user-agent':'Mozilla/5.0'}
            r = requests.get(img_url,headers = kv)
            with open(path,'wb') as f:
                f.write(r.content)           #将二进制图像文件写入本地
            print('图片url：'+img_url)
            print('图片'+str(img_num)+'爬取成功')
            
        else:
            print('图片'+str(img_num)+'已存在') 
    except:
        print('爬取失败')

def item_input(kw):
   #http0 =  'https://www.amazon.cn/s/ref=sr_pg_1?rh=n%3A2016156051%2Ck%3A'   # -> rh=i%3Aaps%2Ck%3A
    http0 = 'https://www.amazon.cn/s/ref=sr_pg_1?rh=i%3Aaps%2Ck%3A'
    http2 = '&page=1&keywords='
    http3 = '&ie=UTF8&qid=1520509106'
    global category
    category = kw
    kw1 = str(kw.encode())
    kw1 = kw1.replace('\\x','%')
    http1 = kw1.split("'")[1]
    url0 = http0 + http1 + http2 + http1 + http3
    return url0

if __name__ == '__main__':
    kw = input('请输入商品名称:')
    url0 = item_input(kw)
    global img_num
    img_num = 1
    page = 1
    total_flag = 0
    flag = 1
    while flag == True:
        img_urls = get_img_urls(url0)         #获取图像url
        for img_url in img_urls:
            get_pic(img_url,category,img_num,kw) #爬取图像文件到本地
            img_num += 1
        #   if img_num == 200:
        #       flag = 0
        #       break
        
        url0 = url0.replace('pg_'+str(page),'pg_'+str(page+1))
        url0 = url0.replace('page='+str(page),'page='+str(page+1))
        page += 1
        if page>total_url:
            break
    print('*********爬取结束************')


