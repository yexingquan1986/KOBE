import zlib, struct

def read_png(path):
    with open(path, 'rb') as f:
        data = f.read()
    pos = 8
    idat = b''
    w = h = bitd = ctype = None
    while pos < len(data):
        ln = struct.unpack('>I', data[pos:pos+4])[0]
        typ = data[pos+4:pos+8]
        chunk = data[pos+8:pos+8+ln]
        if typ == b'IHDR':
            w, h, bitd, ctype = struct.unpack('>IIBB', chunk[:10])
        elif typ == b'IDAT':
            idat += chunk
        pos += 12 + ln
    raw = zlib.decompress(idat)
    ch = {0:1, 2:3, 3:1, 4:2, 6:4}[ctype]
    stride = w * ch
    rows = []
    prev = bytearray(stride)
    i = 0
    for y in range(h):
        f = raw[i]; i += 1
        line = bytearray(raw[i:i+stride]); i += stride
        if f == 1:
            for j in range(ch, stride):
                line[j] = (line[j] + line[j-ch]) & 255
        elif f == 2:
            for j in range(stride):
                line[j] = (line[j] + prev[j]) & 255
        elif f == 3:
            for j in range(stride):
                a = line[j-ch] if j >= ch else 0
                b = prev[j]
                line[j] = (line[j] + ((a + b) >> 1)) & 255
        elif f == 4:
            for j in range(stride):
                a = line[j-ch] if j >= ch else 0
                b = prev[j]
                c = prev[j-ch] if j >= ch else 0
                p = a + b - c
                pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[j] = (line[j] + pr) & 255
        prev = line
        rows.append(line)
    return w, h, ch, rows

w, h, ch, rows = read_png(r'K:\BBK\_shots\full_mobile2.png')

def runs(y):
    line = rows[y]
    out = []
    start = None
    for x in range(w):
        nw = line[x*ch] < 245 or line[x*ch+1] < 245 or line[x*ch+2] < 245
        if nw and start is None:
            start = x
        elif not nw and start is not None:
            if x - start >= 2:
                out.append((start, x-1))
            start = None
    if start is not None:
        out.append((start, w-1))
    return out

for y in [938, 940, 942, 950, 990, 1000, 1010, 1050]:
    print('y', y, runs(y))
