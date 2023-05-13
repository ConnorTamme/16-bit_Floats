import math as m
"""
A class allowing the storing of a decimal and its corresponding closest 16 bit float
"""
class Float16:
    """
    Initializes the class with a value of 0
    """
    def __init__(self):
        self.decimal = 0
        self.binary = 0
    """
    Sets the value stored based on a decimal
    Parameters:
    decimal: a decimal value
    """
    def setDecimal(self, decimal):
        self.decimal = decimal
        self.binary = self.__convertDecimaltoBinary(decimal)
    """
    Sets the value stored based on a 16 bit float
    Parameters:
    float: a string or integer containing a 16 bit float
    """
    def setFloat(self, float):
        self.binary = float
        self.decimal = self.__convertBinarytoDecimal(float)
    """
    Gets the current 16 bit float value as a string
    """
    def getFloat(self) -> str:
        return str(self.binary).zfill(16)
    """
    Gets the current decimal value as a float
    """
    def getDecimal(self) -> float:
        return float(self.decimal)
    """
    Adds the given decimal value to the current value
    Parameters:
    decimal: a decimal value
    """
    def addDecimal(self, decimal):
        self.decimal = self.decimal + decimal
        self.binary = self.__convertDecimaltoBinary(self.decimal)
    """
    Adds the given 16 bit float to the current value
    Parameters:
    float: a string or integer containing a 16 bit float
    """
    def addFloat(self, float):
        self.addDecimal(self.__convertBinarytoDecimal(float))
    """
    Multiplies the current value by the given decimal value
    Parameters:
    decimal: a decimal value
    """
    def multiplyDecimal(self, decimal):
        self.decimal = self.decimal * decimal
        self.binary = self.__convertDecimaltoBinary(self.decimal)
    """
    Multiplies the current value by the given 16 bit float
    Parameters:
    float: a string or integer containing a 16 bit float
    """
    def multiplyFloat(self, float):
        self.multiplyDecimal(self.__convertBinarytoDecimal(float))
    """
    Divides the current value by the given decimal value
    Parameters:
    decimal: a decimal value
    """
    def divideDecimal(self, decimal):
        self.decimal = self.decimal / decimal
        self.binary = self.__convertDecimaltoBinary(self.decimal)
    """
    Divides the current value by the given 16 bit float
    Parameters:
    float: a string or integer containing a 16 bit float
    """
    def divideFloat(self, float):
        self.divideDecimal(self.__convertBinarytoDecimal(float))
    """
    Subtracts the given decimal value from the current value
    Parameters:
    decimal: a decimal value
    """
    def subDecimal(self, decimal):
        self.decimal = self.decimal - decimal
        self.binary = self.__convertDecimaltoBinary(self.decimal)
    """
    Adds the given 16 bit float to the current value
    Parameters:
    float: a string or integer containing a 16 bit float
    """
    def subFloat(self, float):
        self.subDecimal(self.__convertBinarytoDecimal(float))
    """
    Converts the given decimal number into a 16 bit float
    Parameters:
    decimal: a decimal value
    """
    def __convertDecimaltoBinary(self, decimal):
        #Determines sign bit
        if (decimal < 0):
            sign = 1 * 10 ** 15
            decimal = decimal * -1
        else:
            sign = 0
        
        integer = decimal // 1
        fraction = decimal % 1
        #Determines the binary value of the integer part of the number
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
        #Determines the binary value of the decimal part of the number
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
        #Determines the value of the exponent
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
        if (exponent != 0): #Checks if the number is a denorm
            bin -= 1
        else:
            bin = bin / 10
        #Determines the value of the exponent bits
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
    """
    Converts the given 16 bit float into a decimal number
    Parameters:
    float: a string or integer containing a 16 bit float
    """
    def __convertBinarytoDecimal(self, binary):
        binary = int(binary)
        sign = binary // (1 * 10 ** 15)
        exponent = (binary // (1 * 10 ** 10)) % (10 ** 5)
        fraction = binary % (10 ** 10)
        decExp = 0
        power = 0
        #Determines the value of the exponent and applies the to fraction
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
        #Determines the value of the integer part of the value
        while (whole >= 1):
            if ((whole // (1)) % 10 == 1):
                decInt = decInt + 2 ** (power)
            whole = whole / 10
            power += 1
        decPart = 0
        power = 1
        #Determines the value of the decimal part of the value
        while (part != 0):
            part = part * 10
            part = round(part, 24)
            if (part // 1 >= 1):
                part = part - 1
                decPart = decPart + 0.5 ** (power)
            power += 1
            if (power > 24):
                break
        if (sign == 1): #Applies the sign
            return (decInt + decPart) * -1
        return (decInt + decPart)

x = Float16()
x.setDecimal(3)
print(str(x.getDecimal()) + ", " + x.getFloat())
x.addDecimal(3.5)
print(str(x.getDecimal()) + ", " + x.getFloat())
x.multiplyDecimal(3)
print(str(x.getDecimal()) + ", " + x.getFloat())
x.divideDecimal(3)
print(str(x.getDecimal()) + ", " + x.getFloat())
x.subDecimal(3.5)
print(str(x.getDecimal()) + ", " + x.getFloat())

y = Float16()
y.setFloat("0110010000000000")
print(str(y.getDecimal()) + ", " + y.getFloat())
y.addFloat("0110001110100000")
print(str(y.getDecimal()) + ", " + y.getFloat())
y.multiplyFloat("0011111000000000")
print(str(y.getDecimal()) + ", " + y.getFloat())
y.divideFloat("0100001000000000")
print(str(y.getDecimal()) + ", " + y.getFloat())