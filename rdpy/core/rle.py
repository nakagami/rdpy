
# https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rdpbcgr/b6a3f5c2-0804-4c10-9d25-a321720fd23e

def CVAL(p):
    return p[0], p[1:]


def process_plane(input_data, width, height, output, j):
    ln = len(input_data)

    lastline = 0
    indexh = 0
    i = 0
    while indexh < height:
        thisline = j + (width * height * 4) - ((indexh + 1) * width * 4)
        color = 0
        indexw = 0
        i = thisline

        if lastline == 0:
            while indexw < width:
                code, input_data = CVAL(input_data)
                replen = code & 0x0F
                collen = (code >> 4) & 0xF
                revcode = (replen << 4) | collen
                if revcode <= 47 and revcode >= 16:
                    replen = revcode
                    collen = 0
                while collen > 0:
                    color = CVAL(input_data)
                    output[i] = color
                    i += 4
                    indexw += 1
                    collen -= 1
                while replen > 0:
                    output[i] = color
                    i += 4
                    indexw += 1
                    replen -= 1
        else:
            while indexw < width:
                code, input_data = CVAL(input_data)
                replen = code & 0x0F
                collen = (code >> 4) & 0x0F
                revcode = (replen << 4) | collen
                if revcode <= 47 and revcode >=16:
                    replen = revcode
                    collen = 0
                while collen >0:
                    x, input_data = CVAL(input_data)
                    if x & 1 != 0:
                        x = x >> 1
                        x = x + 1
                        color = -x
                    else:
                        x = x >> 1
                        color = x
                    x = output[indexw * 4 + lastline] + color
                    output[i] = x
                    i += 4
                    indexw += 1
                    collen -= 1
                while replen > 0:
                    x = output[indexw * 4 + lastline] + color
                    output[i] = x
                    i -= 4
                    indexw += 1
                    replen -= 1
        indexh += 1
        lastline = thisline

    return ln - len(input_data), input_data


def bitmap_decompress4(input_data, width, height):
    BPP = 4
    size = width * height * BPP
    output = [0] * size
    return output

    code, input_data = CVAL(input_data)
#    assert code == 0x10

    total = 1

    process_ln, input_data = process_plane(input_data, width, height, output, 3)
    total += process_ln

    process_ln, plane, input_data = process_plane(input_data, width, height, 2)
    total += process_ln

    process_ln, plane, input_data = process_plane(input_data, width, height, 1)
    total += process_ln

    process_ln, plane, input_data = process_plane(input_data, width, height, 0)
    total += process_ln

    assert size == total

    return output
