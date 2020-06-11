# Python-Source-Code-Plagiarism-Detection
Calculate similarity using text-based apprroaches and attribute-counting. Attribute-counting is based on lexical analysis.

Lexical analysis is designed for python 3.6

基于文本相似度和属性计数检测python源码文件相似度。包含一个python词法分析器以驱动属性计数。

词法分析器参考python 3.6的词法规则设计

生成的结果文件包含源码文件夹内所有文件两两双向对比的结果。如果要寻找某个文件的潜在抄袭文件，方法如下：

1. 将这个文件和其他待对比文件放在同一文件夹并运行主程序。

2. 得到结果csv文件后，单独运行group.py分析结果csv文件

3. 输入使用的算法阈值和标准参考文件的文件名后即可得到较高相似度的文件和它们和标准文件的相似度

推荐阈值：

函数内顺序对比：0.65

函数内行最大相似：0.6

特征计数（默认权值）：0.3
