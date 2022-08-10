def give_remainder_dict(dividend, divisor, digits):
    # Initialize the dictionary
    frequency_dict = {}
    #find quotient and remainder
    quotient=dividend//divisor
    remainder=dividend%divisor
    #convert it into the string
    decimal=str(remainder)
    last=remainder*10
    #iterate till the length of the string is equal to the number of digits
    for i in range(digits):
        #if the last digit is less than divisor then multiply it by 10 and divide by divisor and add it to the last
        if(last<divisor):
            last=last*10
            decimal=decimal+str(last//divisor)
            #update the remainder
            last=last%divisor
        else:
            #if the last digit is greater than divisor then add it to the decimal and update the last
            decimal=decimal+str(last//divisor)
            last=last%divisor
    #removing the first element of the string
    decimal=decimal[1:]
    #make all the frequencies of the digits equal to zero
    for i in range(10):
        frequency_dict[str(i)]=0
    #update the frequencies of the digits
    for i in decimal:
        if i in frequency_dict:
            frequency_dict[i]+=1
    #return the dictionary
    return frequency_dict

def main():
    dividend = int(input("Enter the dividend: "))
    divisor = int(input("Enter the divisor: "))
    digits = int(input("Enter the number of digits: "))
    #call the function and print the dictionary
    frequency_dict = give_remainder_dict(dividend, divisor, digits)
    print(frequency_dict)

__name__ == "__main__"
main()
