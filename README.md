# deltaMushToSkinCluster

自动将Delta Mush的变形效果转换到SkinCluster上，从而减小场景开销。

## 联系方式:
* 作者: [Godfrey Huang](http://www.cgenter.com)
* 邮箱: <godfreyhuang@cgenter.com>

## 环境需求: 
Maya 2014 x64+, Windows, and OS X

## 安装:
####自动安装

* 拖拽"install.mel"到maya窗口，当前shelf工具栏会新增命令按钮

####手动安装

* 拷贝module/deltaMushToSkinCluster.mod文件到maya的设置文件夹路径（如：C:\Users\你的用户名\Documents\maya）下的module文件夹下（如没有module文件夹则新建）

* 编辑deltaMushToSkinCluster.mod文件，替换"REPLACE_YOUR_PATH"为本插件的安装目录（如：E:\dev）,编辑后mod文件像下面一样
> +deltaMushToSkinCluster 1.0 E:/dev/deltamushtoskincluster

##使用
* 选择带deltaMush变形器的polygon物体后，执行shelf按钮或以下python代码进行自动转换
```python
import dm2sc.convert as convert
convert.main()
```