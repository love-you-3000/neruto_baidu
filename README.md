# Scrapy抓取并下载火影忍者壁纸

## 本项目通过scrapy框架实现百度图片中关键词为火影忍者的图片的爬取，并将结果存放在mongo和下载到本地

### 1、抓取分析

        我们首先在百度图片中输入：火影忍者壁纸，可以看出来页面输入Ajax请求，打开谷歌开发者工具，查看f12，得到如下结果：

        我们可以发现其实只有最后的pn参数发生了变化，所以我们只需要对pn进行更新即可。
        然后我们再看每个url下的json数据长什么样：

![图1](https://raw.githubusercontent.com/love-you-3000/neruto_baidu/master/image_floder/1.jpg)

        可以发现每个图片的信息都存放在这些data中，然后我们打开看一下我们需要的数据在哪里：
	
![图2](https://raw.githubusercontent.com/love-you-3000/neruto_baidu/master/image_floder/2.jpg)
        可以发现我们要爬取的标题和图片链接在键名为fromPageTitleEnc和hoverURL中：
	
![图3](https://raw.githubusercontent.com/love-you-3000/neruto_baidu/master/image_floder/3.jpg)
        于是我们就可以开始我们的抓取工作了。


### 2、新建项目

	首先需要新建一个项目，这里不再赘述。

### 3、构造请求

	具体代码spiders中的images.py中。
	这里需要现在settings创建MAX_PAGE,即爬取页数。其中需要将ROBOTISTXT_OBEY修改为False，不然无法抓取。
	
### 4、提取信息

	具体代码在item中。
	
### 5、保存数据

	在pipelines.py中实现保存数据到mongo。
![图4](https://raw.githubusercontent.com/love-you-3000/neruto_baidu/master/image_floder/4.jpg)

### 6、下载数据

	需要重写ImagePipline类，之后就可以爬取了。

	展示一下结果：
	
![图5](https://raw.githubusercontent.com/love-you-3000/neruto_baidu/master/image_floder/5.jpg)



# 大学生一枚，记录一下学习过程，如果有看官乐意，赏个stars我也不介意，哈哈哈哈哈。
![图6](https://raw.githubusercontent.com/love-you-3000/neruto_baidu/master/image_floder/6.jpg)
        
