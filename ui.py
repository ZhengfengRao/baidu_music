# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Wed Jan 23 11:07:14 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!
import sys
from PySide import QtCore, QtGui
from PySide.QtCore import *
from PySide.QtGui import *
from baidu_music import BaiduMusic
import winsound
class VerifyDialog(QtGui.QDialog):
    def __init__(self,filename):
        super(VerifyDialog, self).__init__()
        mainLayout = QtGui.QHBoxLayout()
        self.label = QLabel()
        self.edit = QLineEdit()
        self.ok = QPushButton(u"提交")
        self.text=""
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.edit)
        mainLayout.addWidget(self.ok)
        self.setLayout(mainLayout)
        self.setWindowTitle(u"验证")
        self.label.setPixmap(QPixmap(filename))
        self.ok.clicked.connect(self.clicked)
        winsound.Beep(500,1216)
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.on_timer)
        self.timer.start( 1000*60*15 )
    def on_timer(self):
        self.close()
    def clicked(self):
        self.text = self.edit.text()
        self.close()

class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)

        root = QVBoxLayout()
        self.label = QLabel()
        self.label.setText(u'''<p><span style="font-size: 16px;"><strong>&nbsp;命令参考</strong></span></p>
<hr />
<p>&nbsp;</p>
<table style="height: 49px; width: 938px;" border="0">
<tbody>
<tr>
<td><span style="color: #0000ff; font-size: 16px;"><strong>命令</strong></span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="color: #0000ff; font-size: 16px;"><strong>说明</strong></span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="color: #0000ff; font-size: 16px;"><strong>例子</strong></span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="color: #0000ff; font-size: 16px;"><strong>例子说明</strong></span></td>
</tr>
<tr>
<td>
<p dir="ltr"><span style="font-size: 16px; color: #0000ff;">-s 歌手1,歌手2,...歌手N</span></p>
</td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td>
<p dir="ltr"><span style="font-size: 16px;">|</span></p>
</td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">下载歌手的所有专辑</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">|</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;"><em>-s 周华健,莫文蔚</em></span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">|</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">下载周华健和莫文蔚的所有专辑</span></td>
</tr>
<tr>
<td>
<p dir="ltr"><span style="font-size: 16px; color: #0000ff;">-a 歌手:专辑1,歌手:专辑2,歌手:专辑N</span></p>
</td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td>
<p dir="ltr"><span style="font-size: 16px;">|</span></p>
</td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">下载歌手的具体专辑</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">|</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;"><em>-s 曹方:黑色香水</em></span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">|</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">下载曹方的黑色香水专辑</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">-d 保存路径</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">|</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">设置歌曲的下载路径</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">|</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;"><em>-d d:\mp3</em></span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">|</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">保存到D盘mp3文件夹下面</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">-l 列表1,列表2,...列表N</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">|</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">下载百度的榜单</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">|</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;"><em>-l new,folk</em></span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">|</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px;">下载新歌TOP100和民谣榜</span></td>
</tr>
</tbody>
</table>
<p><span style="font-size: 16px;">列表参考</span></p>
<hr />
<p>&nbsp;</p>
<table style="height: 222px; width: 596px;" border="0" align="left">
<tbody>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">dayhot</span></td>
<td><span style="font-size: 16px; color: #0000ff;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">歌曲TOP500</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">new</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">新歌TOP100</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">omei</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">欧美金曲榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">huayu</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">华语金曲榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">yingshijinqu</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">影视金曲榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">lovesong</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">情歌对唱榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">netsong</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">网络歌曲榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">oldsong</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">经典老歌榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">rock</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">摇滚榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">jazz</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">爵士榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">folk</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">民谣榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">ktv</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">KTV热歌榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">billboard</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">Billboard</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">ukchart</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">UK Chart</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">hito</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">Hito中文榜</span></td>
</tr>
<tr>
<td><span style="font-size: 16px; color: #0000ff;">chizha</span></td>
<td><span style="font-size: 16px;">&nbsp;</span></td>
<td><span style="font-size: 16px; color: #0000ff;">叱咤歌曲榜</span></td>
</tr>
</tbody>
</table>
<hr />
<h1><span style="font-size: 16px;">完整的例子</span></h1>
<p><span style="font-size: 16px;">下载郑智化,仓木麻衣的所有专辑,下载KTV热歌榜,经典老歌榜,下载滨崎步的Next Level专辑和张惠妹姐妹这张专辑</span></p>
<p><span style="font-size: 16px;">最后保存在D盘下mp3文件夹里面</span></p>
<p><span style="font-size: 16px;">&nbsp;<span style="color: #0000ff;"><em>-a 郑智化,仓木麻衣 -l ktv,oldsong -a 滨崎步:Next Level,张惠妹:姐妹 -d d:\mp3</em></span></span></p>''')

        self.resize(680,self.y()*2)
        self.setWindowTitle("Baidu Music")
        h_layout = QHBoxLayout()
        self.line_edit = QLineEdit()
        font = QtGui.QFont()
        font.setPointSize(16)
        self.line_edit.setFont(font)

        self.line_edit.setText(u"-s 周华健 -d music")
        self.push_button = QPushButton()
        self.push_button.setText(u"下载")
        self.push_button.setFont(font)
        h_layout.addWidget(self.line_edit)
        h_layout.addWidget(self.push_button)
        root.addLayout(h_layout)
        root.addWidget(self.label)
        self.setLayout(root)
        self.push_button.clicked.connect(self.clicked)
        self.baidu_music = BaiduMusic()
        self.baidu_music.setUI(self)

    def clicked(self):
        self.push_button.setEnabled(False)
        command = self.line_edit.text()
        self.baidu_music.invoke_command(command)
        self.push_button.setEnabled(True)

    def verify(self,filename):
        dia = VerifyDialog(filename)
        dia.exec_()
        return dia.text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainDialog()
    form.show()
    sys.exit(app.exec_())