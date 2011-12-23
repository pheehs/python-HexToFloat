#!/usr/bin/env python
#-*- coding:utf-8 -*-

import struct

    
def toBinary(decimal, bit):
    if decimal == 0: return '0'*bit
    bin_str = ""
    while decimal > 0:
        bin_str += str(decimal % 2)
        decimal >>= 1
    if len(bin_str) < bit:
        return "0"*(bit-len(bin_str)) + bin_str[::-1]
    elif len(bin_str) == bit:
        return bin_str[::-1]
    else:
        raise ValueError, "Parameter should be under %sbit!" % bit

float_little = lambda x: "".join([hex(ord(struct.pack("f", x)[i]))[1:].replace("x", " ") for i in xrange(4)]).strip()
float_big = lambda x: "".join([hex(ord(struct.pack(">f", x)[i]))[1:].replace("x", " ") for i in xrange(4)]).strip()

double_little = lambda x: "".join([hex(ord(struct.pack("d", x)[i]))[1:].replace("x", " ") for i in xrange(8)]).strip()
double_big = lambda x: "".join([hex(ord(struct.pack(">d", x)[i]))[1:].replace("x", " ") for i in xrange(8)]).strip()

f2i = lambda i:struct.unpack("I", struct.pack("f", i))[0]
d2i = lambda i:struct.unpack("Q", struct.pack("d", i))[0]


def HexToFloat(hex_int):
    print "[-- HexToFloat --]"
    mask_sign = 0x80000000 # 0b10000000000000000000000000000000
    mask_exponent = 0x7f800000 # 0b[0111][1111][1000][0000][0000][0000][0000][0000]
    mask_fraction = 0x7fffff # 0b[0000][0000][0111][1111][1111][1111][1111][1111]

    print "Dump(little endian):", float_little(hex_int)
    print "Dump(big endian):", float_big(hex_int)
    
    sign = (hex_int & mask_sign) >> 31
    print "Sign(bin):", toBinary(sign, 1)
    exponent = int(((hex_int & mask_exponent) >> 23) - 127)
    print "Exponent(bin):", toBinary(exponent, 8), "(%s = %d)" % (hex(exponent), exponent)
    fraction = toBinary(hex_int & mask_fraction, 23)
    print "Fraction(bin):", fraction, "(%s)" % hex(hex_int & mask_fraction)

    approx_base = (-1) ** sign * 2 ** exponent
    print "No fraction:", approx_base, "<= f <", approx_base*2
    
    fraction_list = [1.]
    for i in xrange(23):
        if int(fraction[i]):
            fraction_list.append(1. / 2**(1+i))
        else:
            fraction_list.append(0)

        print "Approximation(fraction:1/2^%d):" % (1+i), \
            approx_base * sum(fraction_list), \
            "<= f <", \
            approx_base * (sum(fraction_list) + 1. / 2**(1+i))
    print
    result = approx_base * sum(fraction_list)
    return result

def HexToDouble(hex_int):
    print "[-- HexToDouble --]"
    mask_sign = 0x8000000000000000
    mask_exponent = 0x7ff0000000000000
    mask_fraction = 0x000fffffffffffff
    
    print "Dump(little endian):", double_little(hex_int)
    print "Dump(big endian):", double_big(hex_int)
    
    sign = (hex_int & mask_sign) >> 63
    print "Sign(bin):", toBinary(sign, 1)
    exponent = int(((hex_int & mask_exponent) >> 52) - 1023)
    print "Exponent(bin):", toBinary(exponent, 11), "(%s = %d)" % (hex(int(exponent)), exponent)
    fraction = toBinary(hex_int & mask_fraction, 52)
    print "Fraction(bin):", fraction, "(%s)" % hex(hex_int & mask_fraction)
    
    approx_base = (-1) ** sign * 2 ** exponent
    
    fraction_list = [1.]
    for i in xrange(52):
        if int(fraction[i]):
            fraction_list.append(1. / 2**(1+i))
        else:
            fraction_list .append(0)
        
        print "Approximation(fraction:1/2^%d):" % (1+i), \
            approx_base * sum(fraction_list), \
            "<= d <", \
            approx_base * (sum(fraction_list) + 1. / 2**(1+i))
    print
    result = approx_base * sum(fraction_list)
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Error!\n"
        print "Usage: %s [floating-point number]\n" % sys.argv[0]
    
    HexToFloat(f2i(float(sys.argv[1])))
    HexToDouble(d2i(float(sys.argv[1])))
