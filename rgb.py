#! /usr/bin/python
## RGB color conversion scrpit

import sys

class colors :
    BLK="\033[38;2;0;0;0m"
    GRY="\033[38;2;128;128;128m"
    WHT="\033[38;2;255;255;255m"
    RST="\033[0m"

if len(sys.argv)==1 :
    inpt=input("\nEnter the color value that you want to convert > ")
else :
    inpt=sys.argv[1]
if (inpt=="-h") | (inpt=="--help") :
    print("Usage : rgb [color]\n\n\
Where \"color\" can be any of these three type of data : \n\
    - A hexadecimal value in the form of \"#hhhhhh\" or \"hhhhhh\"\n\
    - An array of normalized values in the form of \"d.d,d.d,d.d\"\n\
    - An array of decimal 8 bit values in the form of \"d,d,d\"\n\n\
Note that the arrays can have a dimension different to 3")
    exit(0)

## conversion functions
#only 3 are needed
def hexto8bit(h) :
    bit = []
    for i in range(len(h)//2) :
        bit.append(int(h[0+i*2:2+i*2],16))
    return bit

def bit8tonorm(bit) :
    return [round(bit[i]/255,3) for i in range(len(bit))]

def normtohex(n) :
    h = ''
    for i in range(len(n)) :
        htemp = hex(round(n[i]*255))[2:]
        h = h + ("0"+htemp)*(len(htemp)!=2) + (htemp)*(len(htemp)==2) #avoids an if statement
    return h

if "." in inpt :
    #type = norm
    print("\nInput identified as normalized values",inpt)
    inpt=inpt.split(",")
    inpt=list(map(float,inpt))
    h=normtohex(inpt)
    bit=hexto8bit(h)
    print(f"\n• Hexadecimal :          #{h}")
    print(f"• 8 bit decimal values : {bit}".replace(']','').replace('[',''))
    if len(bit) >= 3 :
        print(f"\n                           \
{colors.BLK}  🭁████🭌\
{colors.GRY}  🭁████🭌\
{colors.WHT}  🭁████🭌\
{colors.RST}")
        print(f"The color looks like this :\
{colors.BLK}  ██\033[38;2;{bit[0]};{bit[1]};{bit[2]}m██{colors.BLK}██\
{colors.GRY}  ██\033[38;2;{bit[0]};{bit[1]};{bit[2]}m██{colors.GRY}██\
{colors.WHT}  ██\033[38;2;{bit[0]};{bit[1]};{bit[2]}m██{colors.WHT}██")
        print(f"                           \
{colors.BLK}  🭒████🭝\
{colors.GRY}  🭒████🭝\
{colors.WHT}  🭒████🭝\
{colors.RST}\n")
elif "," in inpt :
    #type = 8bit
    print("\nInput identified as 8 bit decimal values",inpt)
    inpt=inpt.split(",")
    inpt=list(map(int,inpt))
    n=bit8tonorm(inpt)
    h=normtohex(n)
    print(f"\n• Normalized values : {n}".replace(']','').replace('[',''))
    print(f"• Hexadecimal :       #{h}")
    if len(inpt) >= 3 :
        print(f"\n                           \
{colors.BLK}  🭁████🭌\
{colors.GRY}  🭁████🭌\
{colors.WHT}  🭁████🭌\
{colors.RST}")
        print(f"The color looks like this :\
{colors.BLK}  ██\033[38;2;{inpt[0]};{inpt[1]};{inpt[2]}m██{colors.BLK}██\
{colors.GRY}  ██\033[38;2;{inpt[0]};{inpt[1]};{inpt[2]}m██{colors.GRY}██\
{colors.WHT}  ██\033[38;2;{inpt[0]};{inpt[1]};{inpt[2]}m██{colors.WHT}██")
        print(f"                           \
{colors.BLK}  🭒████🭝\
{colors.GRY}  🭒████🭝\
{colors.WHT}  🭒████🭝\
{colors.RST}\n")
else :
    #type = hex
    if inpt[0]=='#' :
        inpt=inpt[1:]
    print("\nInput identified as hex value #",inpt,sep='')
    bit=hexto8bit(inpt)
    n=bit8tonorm(bit)
    print(f"\n• 8 bit decimal values : {bit}".replace(']','').replace('[',''))
    print(f"• Normalized values :    {n}".replace(']','').replace('[',''))
    if len(bit) >= 3 :
        print(f"\n                           \
{colors.BLK}  🭁████🭌\
{colors.GRY}  🭁████🭌\
{colors.WHT}  🭁████🭌\
{colors.RST}")
        print(f"The color looks like this :\
{colors.BLK}  ██\033[38;2;{bit[0]};{bit[1]};{bit[2]}m██{colors.BLK}██\
{colors.GRY}  ██\033[38;2;{bit[0]};{bit[1]};{bit[2]}m██{colors.GRY}██\
{colors.WHT}  ██\033[38;2;{bit[0]};{bit[1]};{bit[2]}m██{colors.WHT}██")
        print(f"                           \
{colors.BLK}  🭒████🭝\
{colors.GRY}  🭒████🭝\
{colors.WHT}  🭒████🭝\
{colors.RST}\n")
