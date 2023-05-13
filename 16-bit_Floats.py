import math as m
class Float16:
    def __init__(self):
        self.decimal = 0
        self.binary = 0
    def setDecimal(self, decimal):
        self.decimal = decimal
        self.binary = self.__convertDecimaltoBinary(decimal)
    def setBinary(self, binary):
        self.binary = binary
        self.decimal = self.__convertBinarytoDecimal(binary)
    def getBinary(self):
        return str(self.binary).zfill(16)
    def getDecimal(self):
        return self.decimal
    def addDecimal(self, decimal):
        self.decimal = self.decimal + decimal
        self.binary = self.__convertDecimaltoBinary(self.decimal)
    def addBinary(self, binary):
        self.addDecimal(self.__convertBinarytoDecimal(binary))
    def multiplyDecimal(self, decimal):
        self.decimal = self.decimal * decimal
        self.binary = self.__convertDecimaltoBinary(self.decimal)
    def multiplyBinary(self, binary):
        self.multiplyDecimal(self.__convertBinarytoDecimal(binary))
    def divideDecimal(self, decimal):
        self.decimal = self.decimal / decimal
        self.binary = self.__convertDecimaltoBinary(self.decimal)
    def divideBinary(self, binary):
        self.divideDecimal(self.__convertBinarytoDecimal(binary))
    def subDecimal(self, decimal):
        self.decimal = self.decimal - decimal
        self.binary = self.__convertDecimaltoBinary(self.decimal)
    def subBinary(self, binary):
        self.subDecimal(self.__convertBinarytoDecimal(binary))
    def __convertDecimaltoBinary(self, decimal):
        if (decimal < 0):
            sign = 1 * 10 ** 15
            decimal = decimal * -1
        else:
            sign = 0
        integer = decimal // 1
        fraction = decimal % 1
        binInteger = 0
        power = -1
        while (integer > 0):
            integer = integer / 2
            if (integer % 1 == 0):
                binInteger = binInteger / 10
            else:
                integer = m.floor(integer)
                binInteger = (binInteger / 10) + 1
            power += 1
        binInteger = binInteger * 10 ** power
        binInteger = m.ceil(binInteger)
        power = 0
        binFraction = 0
        while (fraction != 0):
            fraction = fraction * 2
            if (fraction >= 1):
                fraction -= 1
                binFraction = (binFraction * 10) + 1
            else:
                binFraction = binFraction * 10
            power += 1
            if (power > 100):
                break
        binFraction = binFraction / 10 ** power
        bin = binInteger + binFraction
        exponent = 0
        while (bin < 1 or bin > 2):
            if (bin == 0):
                exponent = -15
                break
            if (bin < 1):
                bin = bin * 10 
                exponent -= 1
            else:
                bin = bin / 10
                exponent += 1
        exponent += 15  
        if (exponent != 0):
            bin -= 1
        else:
            bin = bin / 10
        power = -1
        binExponent = 0
        while (exponent > 0):
            exponent = exponent / 2
            if (exponent % 1 == 0):
                binExponent = binExponent / 10
            else:
                exponent = m.floor(exponent)
                binExponent = (binExponent / 10) + 1
            power += 1
        binExponent = binExponent * 10 ** power
        binExponent = m.floor(round(binExponent, 10))      
        bin = round(bin, 10)
        bin = bin * 10 ** 10
        bin = m.ceil(bin)
        binExponent = binExponent * 10 ** 10
        return sign + binExponent + bin
    def __convertBinarytoDecimal(self, binary: str):
        binary = int(binary)
        sign = binary // (1 * 10 ** 15)
        exponent = (binary // (1 * 10 ** 10)) % (10 ** 5)
        fraction = binary % (10 ** 10)
        decExp = 0
        power = 0
        while (exponent >= 1):
            if ((exponent // (1)) % 10 == 1):
                decExp = decExp + 2 ** (power)
            exponent = exponent / 10
            power += 1
        decExp -= 15
        fraction = fraction / 10 ** 10
        if (decExp == -15):
            fraction = fraction / (10 ** 14)
        else:
            fraction += 1
            fraction = fraction * (10 ** decExp)
            fraction = round(fraction, 10)
        whole = fraction // 1
        part = fraction % 1
        decInt = 0
        power = 0
        while (whole >= 1):
            if ((whole // (1)) % 10 == 1):
                decInt = decInt + 2 ** (power)
            whole = whole / 10
            power += 1
        decPart = 0
        power = 1
        while (part != 0):
            part = part * 10
            part = round(part, 24)
            if (part // 1 >= 1):
                part = part - 1
                decPart = decPart + 0.5 ** (power)
            power += 1
            if (power > 24):
                break
        if (sign == 1):
            return (decInt + decPart) * -1
        return (decInt + decPart)

x = Float16()
x.setDecimal(3)
print(str(x.getDecimal()) + ", " + x.getBinary())
x.addDecimal(3.5)
print(str(x.getDecimal()) + ", " + x.getBinary())
x.multiplyDecimal(3)
print(str(x.getDecimal()) + ", " + x.getBinary())
x.divideDecimal(3)
print(str(x.getDecimal()) + ", " + x.getBinary())
x.subDecimal(3.5)
print(str(x.getDecimal()) + ", " + x.getBinary())

y = Float16()
y.setBinary("0110010000000000")
print(str(y.getDecimal()) + ", " + y.getBinary())
y.addBinary("0110001110100000")
print(str(y.getDecimal()) + ", " + y.getBinary())
y.multiplyBinary("0011111000000000")
print(str(y.getDecimal()) + ", " + y.getBinary())
y.divideBinary("0100001000000000")
print(str(y.getDecimal()) + ", " + y.getBinary())