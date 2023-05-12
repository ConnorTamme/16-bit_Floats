import math as m
class Float16:
    def __init__(self, decimal):
        self.decimal = decimal
        self.binary = self.__convertDecimaltoBinary(decimal)
    #def __init__(self, binary):

    def getFloat(self):
        return str(self.binary).zfill(16)
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
            #if (power > 16):
            #    break
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
        binExponent = m.ceil(binExponent)
        if (exponent != 0):
            bin -= 1
        else:
            bin = bin / 10
        bin = round(bin, 10)
        bin = bin * 10 ** 10
        bin = m.ceil(bin)
        binExponent = binExponent * 10 ** 10
        return sign + binExponent + bin
    
x = Float16(0.00003052)
print(x.getFloat())
