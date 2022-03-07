listq =[1,2,3,4]
listcopy = listq
listgood = listq.copy()
listcopy[1] = 10
listgood[1] = 30
print(listq)

one = 1
two = one
two = 2
print(one)

idx = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'#.split()
letters = [2,8,5,37,38,9,7,5,4,3,1,5,38,37,0,0,10,14,2,13]
password = ""
for index in letters:
    password+= idx[index]
print(password)

#"instructions": "Remove non prime numbers from data then right shift [189th decimal of the constant quantity that
# determines the area of a circle by multiplying it by the radius squared] bits from the remaining numbers, it will
# give you the alphanumeric password of the next level",

# numbers= [ 4994, 57740, 47578, 31074, 25951, 47793, 54605, 55531, 20696, 22082, 25579, 43512, 65059, 25561, 12437, 19766, 42493, 19725, 23261, 45881, 43890, 50978, 51854, 14537, 28745, 37306, 37606, 25367, 47234, 20715, 44869, 58300, 61258, 31528, 25943, 13003, 56191, 6702, 31685, 159, 5326, 48600, 49851, 25841, 25889, 20434, 57008, 13331, 44836, 41353, 4781, 24493, 5061, 25999, 10773, 13789, 60304, 59076, 14723, 41096, 14747, 13487, 62498, 16320, 393, 54971, 14779, 432, 26237, 5670, 26053, 34472, 56235, 56343, 35316, 26293, 37585, 25621, 5168, 14433, 11865, 46015, 25163, 13127, 26321, 14593, 19264, 40301, 45246, 21769, 46297, 53615, 16132, 7340, 65078, 26017, 13033, 62727, 58163, 18213, 47397, 24358, 15860, 22985, 28672, 12983, 35584, 13723, 44271, 40102, 44692, 22299, 64644, 13513, 22101, 12879, 37404, 12025, 15829, 8531, 46175, 27975, 45749, 38775, 12841, 30613, 41185, 12413, 41502, 58972, 6358, 41078, 15429, 21357, 17307, 28659, 12511, 25189, 38822, 64281, 10635, 12553, 14247, 24156, 12401, 48151, 26237, 14935, 54946, 328, 49234, 37774, 59108, 63172, 28397, 43506, 7560, 3939, 13597, 14011, 25303 ]
# numbers = 98, 31418, 25679, 63164, 26317, 13121, 26876, 7153, 13315, 30940, 28118, 24322, 47264, 64294, 2530, 32291, 22508, 59850, 27466, 34257, 65502, 22183, 62152, 62886, 59531, 39162, 4818, 25169, 716, 58135, 15113, 51574, 12911 6711, 45420, 10915, 64479, 25818, 13397, 34011, 47870, 14390, 27985, 10584, 4156, 64413, 14153, 26029, 48088, 12823, 56856, 13493, 8567, 27594, 39982, 4510, 13829, 43126, 3273, 61809, 8186, 53363, 48388, 13621, 39226, 25183, 34634, 13499, 63904, 51115, 54447, 65180, 32810, 18109, 25453, 13751, 63858, 27401, 48717, 12195, 47506, 49421, 14633, 38986, 65463, 52822, 37654, 37498, 54149, 23970, 31996, 12479, 5632, 12589, 25919, 47334, 65084, 34203, 59010, 55357, 26267, 25939, 25402, 58118, 15914, 22435, 23192, 39256, 41796, 29391, 13669 ]
numbers = [ 28187, 31161, 25667, 21032, 21532, 13421, 14060, 21356, 64954, 29783, 29083, 12653, 18345, 33218, 25367, 13577, 26297, 13183, 26041, 37925, 4821, 12791, 22568, 49753, 24774, 47236, 31709, 14197, 14447, 33400, 12763, 38012, 35712, 12659, 19159, 32417, 8757, 46075, 45254, 23601, 481, 6180, 49167, 12189, 26183, 59754, 14481, 35513, 6692, 47437, 56086, 34851, 53110, 48174, 25357, 64169, 20166, 11500, 14251, 25307, 13581, 3421, 14081, 63810, 44888, 19572, 48624, 24039, 52573, 12624, 13463, 17181, 25339, 44458, 35783, 13997, 49536, 611, 11841, 26001, 22705, 50489, 25471, 44746, 25847, 58649, 51774, 14347, 13759, 29993, 14173, 31180, 14387, 61882, 53190, 24841, 38290, 23781, 46369, 65004, 29092, 37845, 25243, 15415, 25981, 14587, 333, 43762, 12517, 25849, 33162, 21533, 47083, 33334, 14071, 518, 30793, 25579, 25303, 65160, 17860, 12391, 33530, 25307, 35070, 38284, 13625, 21201, 14029, 21029, 25609, 12636, 50806, 26227 ]

def isprime(num):
    for n in range(2,int(num**1/2)+1):
        if num%n==0:
            return False
    return True

new_list = []
for number in numbers:
    if(isprime(number)):
        new_list.append(number)
print(new_list)
#one hundred eighty-ninth digit of Pi is 4
bitshift = []
for i in new_list:
    shift = i >> 8
    bitshift.append(shift)
print(bitshift)
ascii = ""
for i in bitshift:
    ascii += chr(i)
print(ascii)

string = open('odoo').read()

password = ""
last_word = ""
for i in string:
    if last_word == ">" and i != ">" and i != "<" and i != "#" and i != "\n":
        password+= i
    if i == "<":
        last_word = "<"
    if i == ">":
        last_word = ">"

print(password)
pwd = []
for i in range(40):
    pwd += "#"

print(pwd)
def r(pwd,text, fr, to, by):
    index = 0
    list(text)
    for i in range(fr, to, by):
        pwd[i] = text[index]
        index += 1
    return pwd
pwd= r(pwd,"b3ba", 0, 4, 1)

pwd=r(pwd, "d8341e81",4, 20, 2)

pwd=r(pwd,"131eccce5", 5, 30, 3)

pwd=r(pwd,"147c85542", 5, 40, 4)

pwd=r(pwd,"81182c", 6, 40, 6)

pwd=r(pwd,"e", 7, 8, 1)

pwd=r(pwd, "478ec59682",10, 40, 3)

pwd=r(pwd,"46c528", 10, 40, 5)

pwd=r(pwd,"68242", 15, 40, 6)

pwd= r(pwd,"cce5881" ,20, 40, 3)

print("".join(pwd))
