# deltaMushToSkinCluster

自动将Delta Mush的变形效果转换到SkinCluster上，从而减小场景开销。

## 联系方式:
* 作者: [Godfrey Huang](https://www.linkedin.com/in/godfreyhuang/)
* 邮箱: <godfrey.huang@udecg.com>

## 环境需求: 
Maya 2018+, Windows x64

## 安装:
####自动安装
* 拖拽"install.mel"到maya窗口，当前shelf工具栏会新增命令按钮
####手动安装
* 拷贝dm2sc.mod文件到maya的设置文件夹路径（如：C:\Users\你的用户名\Documents\maya）下的module文件夹下（如没有module文件夹则新建）
* 编辑dm2sc.mod文件，替换"INSTALL_TARGET_DIR"为本插件的安装目录（如：E:\dev\dm2sc）,编辑后mod文件像下面一样
```mel
+ MAYAVERSION:2018 PLATFORM:win64 dm2sc 1.0 E:/codes/dev/deltamushtoskincluster/release
plug-ins: ./plug-ins/2018/windows/x64

...
...

+ MAYAVERSION:2023 PLATFORM:mac   dm2sc 1.0 E:/codes/dev/deltamushtoskincluster/release
plug-ins: ./plug-ins/2023/osx/x64
```

##使用
* 选择带deltaMush变形器的mesh后，执行shelf按钮或以下python代码进行自动转换
```python
import dm2sc.convert as convert
convert.main()
```