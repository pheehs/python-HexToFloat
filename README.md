## HexToFloat:
c3 f5 48 40(3.14)

### 1. byte order
	- 40 48 f5 c3

### 2. 符号(1bit)
- 一番上の数字が8以上ならマイナス 8未満ならプラス
- マイナスなら8を引いておく
	-  プラス/ 40 48 f5 c3

### 3. 指数部(8bit)
- 上から2桁(0x40)をみる。
	-  40 (deci:)
	
- 0x8(0x10 / 2)で割る [0x2をかけて0x10でわる]
	-  8 (deci:)
	
- 一番後に、3桁目(4)が8未満なら0、8以上なら1を足す。[0x10をかけて0か1をたす]
	-  80
	
- [上から2桁に0x2をかけて、3桁目が8以上なら1を足す]
 0x7f(deci:127)を引く [1を足して0x80を引く]
	-  1

### 4. 仮数部
- 下から6桁(48f5c3)をみて、一番上の桁が8以上なら8を引いて8未満はそのまま
 	- 48 f5 c3
 	
- 一番上の桁:
	4,5,6,7 -> 1/2(0.5)  
        2,3,6,7 -> 1/4(0.25)  
        1,3,5,7 -> 1/8(0.125)  
            
- 二番目以降の桁:
	8,9,A,B,C,D,E,F -> 1/16(0.0625)  
        4,5,6,7,C,D,E,F -> 1/32  
        2,3,6,7,A,B,E,F -> 1/64  
	1,3,5,7,9,B,D,F -> 1/128  
            

### 5. 結果
 符号　* (2^指数部 <= 実際の数 < 2^指数部 * 2)

## まとめ
GH IJ KL MN とすると、
```
switch G:
  case 0~7:
    sign = 0
    switch I:
      case 0:
        exponent = GH0 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 0
      case 1:
        exponent = GH0 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/8(0.125)
      case 2:
        exponent = GH0 * 0x2 / 0x10 + 0x1 - 0x80
        fraction = 1 + 1/4(0.25)
      case 3:
        exponent = GH0 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/4 + 1/8
      case 4:
        exponent = GH0 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/2(0.5)
      case 5:
        exponent = GH0 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/2 + 1/8
      case 6:
        exponent = GH0 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/2 + 1/4
      case 7:
        exponent = GH0 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/2 + 1/4 + 1/8
      case 8:
        exponent = GH8 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1
      case 9:
        exponent = GH8 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/8
      case A:
        exponent = GH8 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/4
      case B:
        exponent = GH8 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/4 + 1/8
      case C:
        exponent = GH8 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/2
      case D:
        exponent = GH8 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/2 + 1/8
      case E:
        exponent = GH8 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/2 + 1/4
      case F:
        exponent = GH8 * 0x2 / 0x10 + 0x1 - 0x80
	fraction = 1 + 1/2 + 1/4 + 1/8
  case 8~F:
    sign = 1
    switch I:
      case 0:
        exponent = (G-8)H * 0x2 + 0x1 - 0x80
	fraction = 1
      case 8:
        exponent = (G-8)H * 0x2 + 0x2 - 0x80
	fraction = 1
```
