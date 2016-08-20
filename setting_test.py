import xml.etree.ElementTree as xml
from xml.dom import minidom

def prettify(value):
    string = xml.tostring(value, 'utf-8')
    reparsed = minidom.parseString(string)
    return reparsed.toprettyxml(indent='\t')

def getFontSize():
    test = xml.parse('setting.xml')

    return int(test.find('font_size').text)

if __name__ == '__main__':
    top = xml.Element('main')

    comment = xml.Comment('フォントサイズ設定')
    top.append(comment)

    font_size = xml.SubElement(top, 'font_size')
    font_size.text = '5'

    tree = xml.ElementTree(top)
    tree.write('setting.xml')

    print(getFontSize())