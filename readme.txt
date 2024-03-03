本意是想做一个直接调用kimi的API帮我读论文的程序，然后发现API太贵了，但kimi网页版免费，就结合chrome和python写了这么个东西

配置环境：
需要chrome浏览器，chromedriver插件（这俩版本需要匹配）
1. 打开chrome浏览器，右上角菜单→帮助→关于chrome→查看chrome版本
2. 打开https://chromedriver.chromium.org/downloads，寻找相应的驱动版本，需要前面两位大版本号与chrome匹配，下载chromedriver
3. 将下载好解压后的chromedriver的exe文件复制到python根目录，这一步不会的话可以参考https://localprod.pandateacher.com/python-manuscript/crawler-html/chromedriver/ChromeDriver.html

准备：
1. 将要读的文献放到一个文件夹下，记下绝对路径为path
2. 将try_chrome.exe和file_location.txt放到同一个目录下
3. 将file_location.txt文件中的路径改成刚刚记下的绝对路径path

运行：
1. 双击try_chrome.exe
2. chrome弹出微信登录的时候登录一下
3. try_chrome.exe当前目录下会生成txt文件夹，读论文输出会以txt形式记录下来

tips：
kimi是一个免费的网站，大伙尽量不要滥用，会给该网站造成太大压力
AI辅助读论文只是一个帮助快速筛选的过程，真正要对论文有理解还是要看原文