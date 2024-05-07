# -*- coding: utf-8 -*-

import concurrent.futures
import os
import subprocess
import sys
import threading
import time
import requests
import webbrowser

from PySide6.QtCore import (QMetaObject, QRect, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QLabel, QLineEdit, QPlainTextEdit, QProgressBar, QPushButton, QButtonGroup, QMainWindow, QFileDialog, QMessageBox)
from gamdl.cli import main as gamdl
from selenium import webdriver
from selenium.webdriver.common.by import By

if_cancel = ['0']
root_path = [os.getcwd()]
complete_process = []


def isCheckURL(url):
    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 200:
            return True
        elif response.status_code == 405:  # Method Not Allowed
            allowed_methods = response.headers.get('Allow', '')
            if 'GET' in allowed_methods:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return True
                else:
                    print(f"URL is not valid. HTTP status code: {response.status_code}")
                    return False
            else:
                print(f"URL is not valid. Neither HEAD nor GET requests are allowed.")
                return False
        else:
            print(f"URL is not valid. HTTP status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"URL is not valid. Error: {e}")
        return False


def _gamdl(option, index):
    if if_cancel[0] != '1':
        complete_process.append(index)
        try:
            gamdl([option])
        except:
            pass


def download_process(option_list: list, index: int):
    concurrent.futures.ThreadPoolExecutor(os.cpu_count() * 9999999).submit(_gamdl, option_list, index)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class _gmadlgui(object):
    def setupUi(self, gmadlgui):
        if not gmadlgui.objectName():
            gmadlgui.setObjectName('gmadlgui')
        gmadlgui.resize(1127, 861)
        font = QFont()
        font.setFamilies(['Arial'])
        font.setPointSize(12)
        gmadlgui.setFont(font)
        gmadlgui.setStyleSheet('QWidget{background: #1a1a1a;}')
        self.label = QLabel(gmadlgui)
        self.label.setObjectName('label')
        self.label.setGeometry(QRect(480, 20, 141, 41))
        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setStyleSheet('QLabel{background: #1a1a1a;color: White;}')
        self.background_1 = QPlainTextEdit(gmadlgui)
        self.background_1.setObjectName('background_1')
        self.background_1.setGeometry(QRect(20, 80, 531, 431))
        self.background_1.setStyleSheet('QPlainTextEdit{background: #232323;}')
        self.background_1.setFrameShape(QFrame.NoFrame)
        self.background_1.setReadOnly(True)
        self.background_1.setBackgroundVisible(False)
        self.background_2 = QPlainTextEdit(gmadlgui)
        self.background_2.setObjectName('background_2')
        self.background_2.setGeometry(QRect(570, 80, 541, 431))
        self.background_2.setStyleSheet('QPlainTextEdit{background: #232323;}')
        self.background_2.setFrameShape(QFrame.NoFrame)
        self.background_2.setReadOnly(True)
        self.background_2.setBackgroundVisible(False)
        self.subTitle1 = QLabel(gmadlgui)
        self.subTitle1.setObjectName('subTitle1')
        self.subTitle1.setGeometry(QRect(170, 100, 201, 31))
        font2 = QFont()
        font2.setPointSize(15)
        self.subTitle1.setFont(font2)
        self.subTitle1.setStyleSheet('QLabel{background: rgba(0, 0, 0, 0); color: White;}')
        self.pasteButton = QPushButton(gmadlgui)
        self.pasteButton.setObjectName(u"pasteButton")
        self.pasteButton.setGeometry(QRect(30, 250, 221, 41))
        font3 = QFont()
        font3.setPointSize(18)
        self.pasteButton.setFont(font3)
        self.pasteButton.setStyleSheet(
            u"QPushButton{color: White; background: Blue;} QPushButton:checked{background: White; color: Black;}")
        self.pasteButton.clicked.connect(self._paste)
        self.URL = QLineEdit(gmadlgui)
        self.URL.setObjectName('URL')
        self.URL.setGeometry(QRect(30, 180, 511, 51))
        self.URL.setStyleSheet('QLineEdit{color: White;}')
        self.subTitle1_2 = QLabel(gmadlgui)
        self.subTitle1_2.setObjectName('subTitle1_2')
        self.subTitle1_2.setGeometry(QRect(200, 320, 161, 31))
        self.subTitle1_2.setFont(font2)
        self.subTitle1_2.setStyleSheet('QLabel{background: rgba(0, 0, 0, 0); color: White;}')
        self.Paths = QLineEdit(gmadlgui)
        self.Paths.setObjectName('Paths')
        self.Paths.setGeometry(QRect(30, 370, 511, 51))
        self.Paths.setStyleSheet('QLineEdit{color: White;}')
        self.OpenDirect = QPushButton(gmadlgui)
        self.OpenDirect.setObjectName('OpenDirect')
        self.OpenDirect.setGeometry(QRect(30, 440, 501, 41))
        self.OpenDirect.setFont(font3)
        self.OpenDirect.setStyleSheet('QPushButton{color: White; background: Blue;} QPushButton:checked{background: White; color: Black;}')
        self.OpenDirect.clicked.connect(self.setOutputpath)
        self._lang_g = QButtonGroup()
        self.lang_select_1 = QCheckBox(gmadlgui)
        self.lang_select_1.setObjectName('lang_select_1')
        self.lang_select_1.setGeometry(QRect(690, 140, 121, 51))
        font4 = QFont()
        font4.setPointSize(20)
        self.lang_select_1.setFont(font4)
        self.lang_select_1.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.lang_select_1.setChecked(False)
        self.lang_select_2 = QCheckBox(gmadlgui)
        self.lang_select_2.setObjectName('lang_select_2')
        self.lang_select_2.setGeometry(QRect(900, 140, 121, 51))
        self.lang_select_2.setFont(font4)
        self.lang_select_2.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.lang_select_2.setChecked(True)
        self.subTitle1_3 = QLabel(gmadlgui)
        self.subTitle1_3.setObjectName('subTitle1_3')
        self.subTitle1_3.setGeometry(QRect(780, 100, 161, 41))
        self.subTitle1_3.setFont(font4)
        self.subTitle1_3.setStyleSheet('QLabel{background: rgba(0, 0, 0, 0); color: White;}')
        self.subTitle1_3.setFrameShape(QFrame.NoFrame)
        self.subTitle1_4 = QLabel(gmadlgui)
        self.subTitle1_4.setObjectName('subTitle1_4')
        self.subTitle1_4.setGeometry(QRect(740, 200, 251, 41))
        self.subTitle1_4.setFont(font4)
        self.subTitle1_4.setStyleSheet('QLabel{background: rgba(0, 0, 0, 0); color: White;}')
        self.subTitle1_4.setFrameShape(QFrame.NoFrame)
        self._down_mod_g = QButtonGroup()
        self.down_mod_2 = QCheckBox(gmadlgui)
        self.down_mod_2.setObjectName('down_mod_2')
        self.down_mod_2.setGeometry(QRect(880, 240, 181, 51))
        self.down_mod_2.setFont(font4)
        self.down_mod_2.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.down_mod_2.setChecked(True)
        self.down_mod_1 = QCheckBox(gmadlgui)
        self.down_mod_1.setObjectName('down_mod_1')
        self.down_mod_1.setGeometry(QRect(680, 240, 121, 51))
        self.down_mod_1.setFont(font4)
        self.down_mod_1.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.subTitle1_5 = QLabel(gmadlgui)
        self.subTitle1_5.setObjectName('subTitle1_5')
        self.subTitle1_5.setGeometry(QRect(790, 290, 111, 41))
        self.subTitle1_5.setFont(font4)
        self.subTitle1_5.setStyleSheet('QLabel{background: rgba(0, 0, 0, 0); color: White;}')
        self.subTitle1_5.setFrameShape(QFrame.NoFrame)
        self.codec_1 = QCheckBox(gmadlgui)
        self.codec_1.setObjectName('codec_1')
        self.codec_1.setGeometry(QRect(610, 330, 61, 51))
        font5 = QFont()
        font5.setPointSize(16)
        self.codec_1.setFont(font5)
        self.codec_1.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self._codecs_g = QButtonGroup()
        self.codec_2 = QCheckBox(gmadlgui)
        self.codec_2.setObjectName('codec_2')
        self.codec_2.setGeometry(QRect(690, 330, 131, 51))
        self.codec_2.setFont(font5)
        self.codec_2.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.codec_2.setChecked(True)
        self.codec_3 = QCheckBox(gmadlgui)
        self.codec_3.setObjectName('codec_3')
        self.codec_3.setGeometry(QRect(830, 330, 161, 51))
        self.codec_3.setFont(font5)
        self.codec_3.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.codec_3.setChecked(False)
        self.codec_4 = QCheckBox(gmadlgui)
        self.codec_4.setObjectName('codec_4')
        self.codec_4.setGeometry(QRect(1000, 330, 91, 51))
        self.codec_4.setFont(font5)
        self.codec_4.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.codec_4.setChecked(False)
        self.codec_5 = QCheckBox(gmadlgui)
        self.codec_5.setObjectName('codec_5')
        self.codec_5.setGeometry(QRect(610, 380, 151, 51))
        self.codec_5.setFont(font5)
        self.codec_5.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.codec_5.setChecked(False)
        self.codec_6 = QCheckBox(gmadlgui)
        self.codec_6.setObjectName('codec_6')
        self.codec_6.setGeometry(QRect(760, 380, 181, 51))
        self.codec_6.setFont(font5)
        self.codec_6.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.codec_6.setChecked(False)
        self.codec_7 = QCheckBox(gmadlgui)
        self.codec_7.setObjectName('codec_7')
        self.codec_7.setGeometry(QRect(960, 380, 91, 51))
        self.codec_7.setFont(font5)
        self.codec_7.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.codec_7.setChecked(False)
        self.codec_8 = QCheckBox(gmadlgui)
        self.codec_8.setObjectName('codec_8')
        self.codec_8.setGeometry(QRect(610, 430, 71, 51))
        self.codec_8.setFont(font5)
        self.codec_8.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.codec_8.setChecked(False)
        self.codec_9 = QCheckBox(gmadlgui)
        self.codec_9.setObjectName('codec_9')
        self.codec_9.setGeometry(QRect(690, 430, 71, 51))
        self.codec_9.setFont(font5)
        self.codec_9.setStyleSheet('QCheckBox{background: rgba(0, 0, 0, 0); color: White;}')
        self.codec_9.setChecked(False)
        self.debug_area = QPlainTextEdit(gmadlgui)
        self.debug_area.setObjectName('debug_area')
        self.debug_area.setGeometry(QRect(20, 520, 1091, 161))
        self.debug_area.setFont(font2)
        self.debug_area.setReadOnly(True)
        self.debug_area.setStyleSheet('QPlainTextEdit{color: White;}')
        self.howset = QPushButton(gmadlgui)
        self.howset.setObjectName("howset")
        self.howset.setGeometry(QRect(40, 770, 221, 41))
        self.howset.setFont(font3)
        self.howset.setStyleSheet("QPushButton{color: White; background: Blue;} QPushButton:checked{background: White; color: Black;}")
        self.mainbar = QProgressBar(gmadlgui)
        self.mainbar.setObjectName("mainbar")
        self.mainbar.setGeometry(QRect(20, 710, 1091, 23))
        self.mainbar.setValue(0)
        self.mainbar.setTextVisible(False)
        self.cancel = QPushButton(gmadlgui)
        self.cancel.setObjectName("cancel")
        self.cancel.setGeometry(QRect(310, 770, 221, 41))
        self.cancel.setFont(font3)
        self.cancel.setStyleSheet("QPushButton{color: White; background: Blue;} QPushButton:checked{background: White; color: Black;}")
        self.star_download = QPushButton(gmadlgui)
        self.star_download.setObjectName("star_download")
        self.star_download.setGeometry(QRect(580, 770, 221, 41))
        self.star_download.setFont(font3)
        self.star_download.setStyleSheet("QPushButton{color: White; background: Blue;} QPushButton:checked{background: White; color: Black;}")
        self.star_download.clicked.connect(self._download)
        self.overwrite = QCheckBox(gmadlgui)
        self.overwrite.setObjectName("overwrite")
        self.overwrite.setGeometry(QRect(850, 760, 111, 51))
        self.overwrite.setFont(font5)
        self.overwrite.setStyleSheet("QCheckBox{background: rgba(0, 0, 0, 0); color: White;}")
        self.overwrite.setChecked(False)
        self.lyrics = QCheckBox(gmadlgui)
        self.lyrics.setObjectName("lyrics")
        self.lyrics.setGeometry(QRect(990, 760, 81, 51))
        self.lyrics.setFont(font5)
        self.lyrics.setStyleSheet("QCheckBox{background: rgba(0, 0, 0, 0); color: White;}")
        self.lyrics.setChecked(False)
        self.overwrite.setText('Overwrite')
        self.lyrics.setText('lyrics')
        self.clear = QPushButton(gmadlgui)
        self.clear.setObjectName("clear")
        self.clear.setGeometry(QRect(1050, 650, 21, 24))
        self.clear.setStyleSheet("QPushButton{background: rgba(0, 0, 0, 0); color: White;}")
        self.pasteButton_2 = QPushButton(gmadlgui)
        self.pasteButton_2.setObjectName("pasteButton_2")
        self.pasteButton_2.setGeometry(QRect(260, 250, 281, 41))
        self.pasteButton_2.setFont(font3)
        self.pasteButton_2.setStyleSheet("QPushButton{color: White; background: Blue;} QPushButton:checked{background: White; color: Black;}")
        self.clear.setText('🗑️')
        self.clear.clicked.connect(self._clear)
        self._lang_g.addButton(self.lang_select_1)
        self._lang_g.addButton(self.lang_select_2)
        self._lang_g.setExclusive(True)
        self._down_mod_g.addButton(self.down_mod_1)
        self._down_mod_g.addButton(self.down_mod_2)
        self._down_mod_g.setExclusive(True)
        self._codecs_g.addButton(self.codec_1)
        self._codecs_g.addButton(self.codec_2)
        self._codecs_g.addButton(self.codec_3)
        self._codecs_g.addButton(self.codec_4)
        self._codecs_g.addButton(self.codec_5)
        self._codecs_g.addButton(self.codec_6)
        self._codecs_g.addButton(self.codec_7)
        self._codecs_g.addButton(self.codec_8)
        self._codecs_g.addButton(self.codec_9)
        self.howset.clicked.connect(self.how_setup)
        self.cancel.clicked.connect(self._cancel)
        self._codecs_g.setExclusive(True)
        self.total = 0
        self.now_count = 0
        if subprocess.run('"{}" --help'.format(os.path.join(root_path[0], 'binary', 'N_m3u8dl-RE')), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
            QMessageBox.critical(None, 'Error!!!', 'Please Install N_m3u8dl-RE')
        if os.path.exists(os.path.join(root_path[0], 'binary', 'mp4decrypt')):
            QMessageBox.critical(None, 'Error!!!', 'Please Install mp4decrypt')
        self.retranslateUi(gmadlgui)

        QMetaObject.connectSlotsByName(gmadlgui)

    def retranslateUi(self, gmadlgui):
        gmadlgui.setWindowTitle('Gamdl-GUI')
        self.label.setText('Gamdl GUI')
        self.subTitle1.setText('Apple Music Share URL')
        self.pasteButton.setText('Paste')
        self.subTitle1_2.setText('Output Directory')
        self.OpenDirect.setText('Output Directory')
        self.lang_select_1.setText('en-US')
        self.lang_select_2.setText('ja-JP')
        self.subTitle1_3.setText('Language')
        self.subTitle1_4.setText('Download Mode')
        self.down_mod_2.setText('nm3u8dlre')
        self.down_mod_1.setText('yt-dlp')
        self.subTitle1_5.setText('Codecs')
        self.codec_1.setText('aac')
        self.codec_2.setText('aac-legacy')
        self.codec_3.setText('aac-he-legacy')
        self.codec_4.setText('aac-he')
        self.codec_5.setText('aac-binaural')
        self.codec_6.setText('aac-he-downmix')
        self.codec_7.setText('atmos')
        self.codec_8.setText('ac3')
        self.codec_9.setText('alac')
        self.howset.setText('How to Setup')
        self.cancel.setText('Cancel')
        self.star_download.setText('Download')
        self.pasteButton_2.setText('Get all music by Artist')

    def _clear(self, _):
        self.debug_area.clear()

    def _paste(self, _):
        if QApplication.clipboard().text().startswith('http'):
            self.URL.setText(QApplication.clipboard().text())
        else:
            if QApplication.clipboard().text() != '':
                if not QApplication.clipboard().text().startswith('http'):
                    QMessageBox.information(None, 'Please set URL or urls.txt', 'please set text file or set url from clipboard!')
                    text = QFileDialog.getOpenFileName(None, 'select urls text file', dir=os.getcwd(), filter='Text files (*.txt)')[0].replace('/', '\\')
                    text = text.replace(os.getcwd(), '.'+os.sep).replace('\\\\', '\\')
                    self.URL.setText(text)

    def setOutputpath(self, _):
        text = QFileDialog.getExistingDirectory(None, 'set output Directory', dir=os.getcwd()).replace('/', '\\')
        text = text.replace(os.getcwd(), '.')
        self.Paths.setText(text)

    def _cancel(self, _):
        if_cancel[0] = '1'
        if not 'Canceled' in self.debug_area.toPlainText():
            self.debug_area.appendPlainText('work Canceled........')
        # self.debug_area.clear()

    def how_setup(self, _):
        webbrowser.open('https://github.com/CrossDarkrix/gamdl-GUI/blob/master/how%20to%20setup.md')

    def _download(self, _):
        complete_process.clear()
        self.mainbar.setValue(0)
        self.total = 0
        lang = ''
        url = []
        codec = ''
        if_cancel[0] = '0'
        if self.lang_select_1.checkState() == Qt.CheckState.Checked:
            lang = 'en-US'
        if self.lang_select_2.checkState() == Qt.CheckState.Checked:
            lang = 'ja-JP'
        if self.URL.text().startswith('http'):
            url = [self.URL.text()]
        if self.URL.text().startswith('http') and ',' in self.URL.text():
            url = self.URL.text().split(',')
        if self.URL.text().startswith('http') and ' ' in self.URL.text():
            url = self.URL.text().split(' ')
        if self.URL.text().startswith('http') and '\r\n' in self.URL.text() or '\n' in self.URL.text():
            url = self.URL.text().splitlines()
        if self.URL.text().startswith('http') and ',' in self.URL.text():
            url = self.URL.text().split(',')
        if self.URL.text().endswith('.txt'):
            url = [_u.replace('\n', '').replace('\r\n', '') for _u in open(self.URL.text(), 'r', encoding='utf-8').readlines()]
        self.url = url
        if self.down_mod_1.checkState() == Qt.CheckState.Checked:
            download_mode = 'ytdlp'
        if self.down_mod_2.checkState() == Qt.CheckState.Checked:
            download_mode = 'nm3u8dlre'
        if self.codec_1.checkState() == Qt.CheckState.Checked:
            codec = 'aac'
        if self.codec_2.checkState() == Qt.CheckState.Checked:
            codec = 'aac-legacy'
        if self.codec_3.checkState() == Qt.CheckState.Checked:
            codec = 'aac-he-legacy'
        if self.codec_4.checkState() == Qt.CheckState.Checked:
            codec = 'aac-he'
        if self.codec_5.checkState() == Qt.CheckState.Checked:
            codec = 'aac-binaural'
        if self.codec_6.checkState() == Qt.CheckState.Checked:
            codec = 'aac-he-downmix'
        if self.codec_7.checkState() == Qt.CheckState.Checked:
            codec = 'atmos'
        if self.codec_8.checkState() == Qt.CheckState.Checked:
            codec = 'ac3'
        if self.codec_9.checkState() == Qt.CheckState.Checked:
            codec = 'alac'
        option = '-l {} -o {} --codec-song {} --download-mode {} --remux-mode ffmpeg --wvd-path {} --nm3u8dlre-path {} --mp4decrypt-path {} --ffmpeg-path {}'.format(lang, self.Paths.text(), codec, download_mode, resource_path('device.wvd'), os.path.join(root_path[0], 'binary', 'mp4decrypt.exe'), os.path.join(root_path[0], 'binary', 'N_m3u8dl-RE.exe'), os.path.join(root_path[0], 'binary', 'ffmpeg.exe'))
        if self.overwrite.checkState() == Qt.CheckState.Checked:
            option = '{} --overwrite'.format(option)
        if self.lyrics.checkState() == Qt.CheckState.Checked:
            option = '{} --no-synced-lyrics'.format(option)
        option_list = ['{} "{}"'.format(option, _u) for _u in url]
        self.total = len(option_list)

        for index, op in enumerate(option_list):
            self.debug_area.appendPlainText('start Downloading Process: {}'.format(index))
            threading.Thread(target=download_process, daemon=True, args=(op, index, )).start()
        self.debug_area.appendPlainText('Please Wait......!')
        concurrent.futures.ThreadPoolExecutor().submit(self.detect)

    def _download2(self, _):
        url = []
        if self.lang_select_1.checkState() == Qt.CheckState.Checked:
            lang = 'en-US'
        if self.lang_select_2.checkState() == Qt.CheckState.Checked:
            lang = 'ja-JP'
        if self.URL.text().startswith('http'):
            url = [self.URL.text()]
        if self.URL.text().startswith('http') and ',' in self.URL.text():
            url = self.URL.text().split(',')
        if self.URL.text().startswith('http') and ' ' in self.URL.text():
            url = self.URL.text().split(' ')
        if self.URL.text().startswith('http') and '\r\n' in self.URL.text() or '\n' in self.URL.text():
            url = self.URL.text().splitlines()
        if self.URL.text().startswith('http') and ',' in self.URL.text():
            url = self.URL.text().split(',')
        if self.URL.text().endswith('.txt'):
            url = [_u.replace('\n', '').replace('\r\n', '') for _u in open(self.URL.text(), 'r', encoding='utf-8').readlines()]
        self.url = url
        _urls = []

        def get_all_music_links():
            for url in self.url:
                if not isCheckURL(url):
                    continue
                if not 'artist' in url:
                    continue
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                driver = webdriver.Chrome(options=options)
                driver.get(url.replace('/see-all?section=top-songs', '') + "/see-all?section=top-songs")
                while True:
                    last_height = driver.execute_script("return document.getElementById('scrollable-page').scrollHeight")
                    driver.execute_script("document.getElementById('scrollable-page').scrollTo(0, document.getElementById('scrollable-page').scrollHeight)")
                    time.sleep(2)
                    new_height = driver.execute_script("return document.getElementById('scrollable-page').scrollHeight")
                    if if_cancel[0] == '1':
                        break
                    if new_height == last_height:
                        break
                elements = driver.find_elements(by=By.XPATH, value="//a[contains(@data-testid, 'track-seo-link')]")
                links = ""
                for element in elements:
                    url = element.get_attribute("href")
                    if 'song' not in url:
                        continue
                    links += url + "\n"
                driver.quit()
                _urls.append(links)
            self.URL.setText('{},{}'.format(self.URL.text(), ','.join(_urls)))
        concurrent.futures.ThreadPoolExecutor().submit(get_all_music_links)


    def detect(self):
        while True:
            try:
                self.mainbar.setValue(min((len(complete_process) / self.total) * 100.0, 100.0))
            except ZeroDivisionError:
                pass
            try:
                if 100 <= min((len(complete_process) / self.total) * 100.0, 100.0):
                    break
            except ZeroDivisionError:
                pass
            if if_cancel[0] == '1':
                break
            time.sleep(0.1)


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = _gmadlgui()
    ui.setupUi(window)
    window.setFixedSize(window.size())
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()