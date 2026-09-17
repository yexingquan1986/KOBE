import struct, sys

def png_size(path):
    with open(path, 'rb') as f:
        data = f.read(33)
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    w, h = struct.unpack('>II', data[16:24])
    return (w, h)

for p in [r'K:\BBK\_shots\高新技术企业成长性分析_desktop.png',
          r'K:\BBK\_shots\高新技术企业成长性分析_mobile.png']:
    print(p, png_size(p))
