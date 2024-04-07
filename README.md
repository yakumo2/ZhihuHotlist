
# Zhihu Hotlist

https://github.com/yakumo2/ZhihuHotlist.git

## 功能

1. 抓取知乎热榜
2. 每次点击`更新`会重新抓一次，新出现在热榜上的内容会标记为`新`
3. 阅读过的内容会标记为`已读`, 也可以直接点击`未读`把当前的条目标记为已读
4. 打开网页或者刷新网页不会重新抓取热榜

虽然是很无聊的功能，但是可以省去刷知乎热榜的时候，并没有更新内容，或者有更新的内容没注意的麻烦。

## 结构
```
- zhihu
    L app.py    #python代码
    L run.sh    #启动app.py
    L saved.json    #自动生成和保存的本地json文件
    L templates
        L index.html    #前端展示

```

## 启动

```
$ python app.py
或者
$ python3 app.py
或者
$ ./run.sh
```

会在`0.0.0.0`的`15000`端口提供web服务。


## codesandbox related


