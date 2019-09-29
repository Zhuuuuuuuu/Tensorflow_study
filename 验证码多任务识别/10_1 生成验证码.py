#验证码生成库
from captcha.image import ImageCaptcha
import numpy as np
from PIL import Image
import random
import sys

number = ['0','1','2','3','4','5','6','7','8','9']
# alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t',
#             'u','v','w','x','y','z']

def random_captcha_text(char_set = number,captcha_size = 4):
    #验证码列表
    captcha_text = []
    for i in range(captcha_size):
        #随机选择字符或者数字
        c = random.choice(char_set)
        #将结果加入到验证码列表
        captcha_text.append(c)
    return captcha_text

#生成字符串对应的验证码
def gen_captcha_text_and_image():
    image = ImageCaptcha()
    #获取随机生成的验证码
    captcha_text = random_captcha_text()
    #把验证码列表转换成字符串
    captcha_text = ''.join(captcha_text)
    #生成验证码
    captcha = image.generate(captcha_text)
    image.write(captcha_text,'captcha/images/' + captcha_text +'.jpg') #写入文件
    
#这里生成的验证码数量会少于10000，因为随机生成会有重名
num = 10000
if __name__ == '__main__':
    for i in range(num):
        gen_captcha_text_and_image()
        # 如用sys.stdout.write() 和\r实现自定义进度条
        sys.stdout.write('\r>> Creating image %d/%d'%(i+1,num))
        sys.stdout.flush() # 强制刷新缓冲区
    sys.stdout.write('\n')
    sys.stdout.flush()

    print("验证码已生成完毕")
#     sys.stdout.write()输出输出不会自动换行，没有end, 可用转义字符自行控制
#     / n
#     换行
#     / r
#     回车到本行首，可刷新输出
# 如用sys.stdout.write()
# 和\r实现自定义进度条