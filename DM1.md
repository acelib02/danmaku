#【弹薄计划】B站弹幕批量爬取
##前言
>B站扩容越来越厉害，弹幕数量增多的同时，弹幕质量也在以肉眼可见的速度下滑。身为一个老B（，我想搞点事情，把弹幕弄得适合自己一点。
>
>最开始是希望做一个人工智能算法，实现对弹幕的动态分析，实现“在我看到不喜欢的弹幕之前，先给我屏蔽了”。这很甲方。
>
>最后因为懒（，决定总之先把弹幕爬下来，有数据了再做EDA好了，就算最后只实现了“生成屏蔽关键词”的功能，对我来说就已经挺nice了。
>
>关于“弹薄”这个概念，有点形而上，如果我能顺利完成所有我觉得必要的代码，我会去知乎上发点魔法笔记。

##任务简介
0202年了，B站改版BV号了，原有的全弹幕装填策略也不好使了，想要大量爬取弹幕，虽然不难，但是各种资料都很散碎，我的编程能力也亟待提升，
所以在弹薄计划的第一阶段，专心解决爬取弹幕问题就好了。

###细分任务
- 练习面向对象程序设计。正好新员工培训在讲java（~~我为什么要学java~~），在python里练一练，改改一缩进到底的习惯
- BV2aid
- aid2cid
- cid2Danmaku
- danmaku2CSV。后续方便存数据库，不过考虑到现阶段能爬到的弹幕数据量并不大，CSV处理也不会太费劲吧。
- 解决过程中遇到的问题

##B站弹幕API
使用requests库，关键方法是requests.get(url, header, cookie)。
由于我最先爬的网站是~~草榴~~静态页面，对动态页面爬取一知半解，这里只聊个人理解：
>我们看到的网页利用查看网页源代码的方法，是可以看到几乎所有显示出来的信息的，从中筛选出需要的内容，就算是静态方法；
>
>网页展示给我们的过程中，包含很多和后端服务器交互、获取数据的过程，从这些过程入手，直接和服务器进行交互，获取数据，就算是动态方法。

通过F12查看网页交互，发现B站页面获得弹幕主要依赖如下几个步骤：
- 输入BV得到页面后，页面中包含aid信息，使用re.findall方法找到；
- 利用"https://www.bilibili.com/widget/getPageList?aid=__"，可以得到弹幕的cid
- 利用"https://api.bilibili.com/x/v1/dm/list.so?oid=__"（其中oid输入前面的cid），可以得到弹幕xml数据。
    - 这里注意到，如果点选历史弹幕，会触发"https://api.bilibili.com/x/v2/dm/history?type=1&oid=173527223&date=YYYY-mm-dd"，返回对应日期的弹幕，输入当天就会返回当天弹幕，所以直接用这个替代基础的获取方法。

##cookie问题
如果爬取历史弹幕，需要用户保持登录状态。
>headers则是用以模拟浏览器登陆，我没有注意到太多具体细节问题，直接拿现有代码做了。

爬虫模拟登陆的最方便方法应该是使用cookie，复杂一些的，包括利用各种cookie库的、利用图像识别库针对滑块的，甚至还有尝试攻破rsa的。
在requests.get方法中加入cookie=mycookie，可以让网站认为我们是登录后的用户，进而获取登录用户才可访问的内容。

###cookie的获取
F12，刷新，网络，查找header，api.vc.bilibili.com域名对应请求头中（firefox打开原始头），Cookie那一项对应的就是用户cookie。
>这东西应该是要保密的

##弹幕数据粗筛
利用前面的方法得到的弹幕数据是XML方法存储的，利用lxml.etree方法进行轻量级分析。etree的xpath方法参考树结构访问。

弹幕xml中，弹幕metadata存于@p内，data用text()方法获取。

- metadata中的信息分别为：'videotime','mode','size','color','unixtime','pool','UID','rowID'，分别对应：
    - videotime：弹幕的时间位置，基于视频长度，单位秒；
    - mode：弹幕模式，1-3滚动弹幕，4底端弹幕，5顶端弹幕，6逆向弹幕，7精准定位，8高级弹幕；
    - size：弹幕大小，12非常小,16特小,18小,25中,36大,45很大,64特别大；
    - color：弹幕的rgb颜色，16777215对应0xFFFFFF；
    - unixtime：发送弹幕的unix时间戳；
    - pool：弹幕池，0普通池 1字幕池 2特殊池；
    - UID：弹幕发送者的用户id；
    - rowID：弹幕数据库中的弹幕编号

其中第一个时间可以转换为float，后续几个可以存为int。注意UID和rowID可能超过int范围，且没有整型化必要，保留即可。
弹幕内容使用utf-8编码。

##弹幕存储
使用CSV存储以上信息，使用csv库完成操作，关键包括csv.writer、csv.reader方法。注意编码。

其中csv.writer方法写入过程如果出现空行，在open操作中对newline关键字进行限定。

##messy code warning!