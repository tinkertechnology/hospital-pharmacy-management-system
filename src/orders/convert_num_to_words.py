def numberToText(no):
    ones = " ,One,Two,Three,Four,Five,Six,Seven,Eight,Nine,Ten,Eleven,Tweleve,Thirteen,Fourteen,Fifteen,Sixteen,Seventeen,Eighteen,Nineteen,Twenty".split(',')
    tens = "Ten,Twenty,Thirty,Fourty,Fifty,Sixty,Seventy,Eighty,Ninety".split(',')
    text = ""
    if len(str(no))<=2:
        if(no<20):
            text = ones[no]
        else:
            text = tens[no//10-1] +" " + ones[(no %10)]
    elif len(str(no))==3:
        text = ones[no//100] +" Hundred " + numberToText(no- ((no//100)* 100))
    elif len(str(no))<=5:
        text = numberToText(no//1000) +" Thousand " + numberToText(no- ((no//1000)* 1000))
    elif len(str(no))<=7:
        text = numberToText(no//100000) +" Lakh " + numberToText(no- ((no//100000)* 100000))
    else:
        text = numberToText(no//10000000) +" Crores " + numberToText(no- ((no//10000000)* 10000000))
    return text

def spellNumber(no):
    # str(no) will result in  56.9 for 56.90 so we used the method which is given below.
    strNo = "%.2f" %no
    n = strNo.split(".")
    rs = numberToText(int(n[0])).strip()
    ps =""
    if(len(n)>=2):
        ps = numberToText(int(n[1])).strip()
        print(ps)
        # rs = ""+ "Rupees" + ps+ " Paisa"  if(rs.strip()=="")  else  (rs + " Rupees " + ps+ " and Paisa").strip()
        rs = ""+ "Rupees" + ps+ " and Paisa"  if(rs.strip()=="")  else  (rs + " Rupees and " + ps+ " " + "Paisa Only").strip()
        print(rs)

        x = rs.replace('and  Paisa Only', "Only")
        print(x)
        
    return x

def generate_amount_words(value):
    return spellNumber(value)