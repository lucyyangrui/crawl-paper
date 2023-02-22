## 一个用于文献调研的小玩意儿

### 使用方法

#### 标准使用方法

首先查看自己的chrome版本，之后在这里下载相应版本的driver，解压出来的.exe文件就放在根目录下就好。

main函数的四个参数：

- 要查询的关键词，比如'multi-modal graph'
- 检索网址，固定的别变。
- 起始要查询的文献“编号”  A
- 结束的文献“编号”  B

PS：最终得到的文献数目大概在 B-A 左右，设置这个参数原因是一次无法打开大量的会议/期刊详情页，（应该有解决办法的，但是懒得找）。建议 B-A 在50上下，也就是一次拿下来50篇文献。

PPS：dblp有反爬，尽量避免多次尝试。

#### 另类使用方法

把你要查询的关键词发给作者，由她代劳哈哈。

---

最终得到的csv文件：

![image-20230222212447870](https://github.com/lucyyangrui/crawl-paper/blob/main/figure/info-csv.png)

然后需要手动上 https://ccf.atom.im/ 检索一下site栏的会议/期刊属于A/B/C，最后可以得到这种：

![image-20230222212640618](https://github.com/lucyyangrui/crawl-paper/blob/main/figure/last.png)



**免责声明**：在不干扰dblp正常工作情况下，仅可用于少量文献且非盈利的检索工作。