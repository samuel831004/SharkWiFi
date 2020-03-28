import struct
import subprocess
import sys
from PyQt5.QtWidgets import (QWidget, QApplication)
import windget_sharkwifi


def get_a_num(c):
    print("get_a_num", c)
    if ord('0') <= ord(c) <= ord('9'):
        return ord(c)-ord('0')
    elif ord('a') <= ord(c) <= ord('f'):
        return ord(c) - ord('a') + 10
    elif ord('A') <= ord(c) <= ord('F'):
        return ord(c) - ord('A') + 10
    else:
        return -1


class SharkWiFi(windget_sharkwifi.Ui_Form):
    def __init__(self, name="__temp_"):
        super().__init__()
        self.file_name = name

    def decode_text_contents(self, content):
        pos = 0
        length = 0
        output = open(self.file_name, 'wb')
        if not output:
            print("error in opening output file")
            return

        while pos < len(content):
            num1 = get_a_num(content[pos])
            pos += 1
            #print(len(content), content[pos], num1, pos)
            if num1 != -1:
                if pos == len(content):  # If this is the last char, write it to bin file
                    length += 1
                    break

                num2 = get_a_num(content[pos])  # Not last char, check if next num is valid
                pos += 1
                if num2 != -1:
                    length += 1
                else:
                    # num2 is -1, only one valid number
                    length += 1

        output.write(struct.pack('<I2H4I', 0xA1B2C3D4, 0x2, 0x4, 0, 0, 0xFFFF, 105))
        output.write(struct.pack('<4I', 0, 0, length, length))

        pos = 0
        while pos < len(content):
            num1 = get_a_num(content[pos])
            pos += 1

            if num1 != -1:
                if len(content) == pos:  # If this is the last char, write it to bin file
                    output.write(struct.pack('B', num1))
                    break

                num2 = get_a_num(content[pos])  # Not last char, check if next num is valid
                pos += 1
                if num2 != -1:
                    output.write(struct.pack('B', (num1 << 4) + num2))
                else:
                    # num2 is -1, only one valid number
                    output.write(struct.pack('B', num1))

        output.close()

    def bt_decode_cmd(self):
        content = self.textEdit.toPlainText()
        print(content)
        if len(content) == 0:
            return
        self.decode_text_contents(content)
        cmd = r"C:\Program Files\Wireshark\Wireshark.exe  %s " % self.file_name
        subprocess.Popen(cmd)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()
    shark = SharkWiFi()
    shark.setupUi(widget)
    shark.pushButton_2.clicked.connect(lambda: shark.bt_decode_cmd())
    widget.show()
    sys.exit(app.exec_())
