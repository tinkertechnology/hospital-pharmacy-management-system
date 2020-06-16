from django.shortcuts import render

#tAmt=None&amt=None&txAmt=None&psc=None&pdc=None&scd=None&pid=None&su=None&fu=None
#localhost:8000/payment/payment_esewa_confirm?tAmt=5&amt=5&txAmt=0&psc=0&pdc=0&pid=1
#localhost:8000/payment/payment_esewa_confirm?tAmt=5&amt=5&txAmt=0&psc=0&pdc=0&pid=ee2c3ca1-696b-4cc5-a6be-2c40d929d453-order1
#localhost:8000/payment/payment_esewa_confirm?tAmt=5&amt=5&txAmt=0&psc=0&pdc=0&pid=ee2c3ca1-696b-4cc5-a6be-2c40d929d453
#localhost:8000/payment/payment_esewa_confirm?tAmt=5&amt=5&txAmt=0&psc=0&pdc=0&pid=air2
#http://localhost:8000/payment/payment_esewa_confirm?tAmt=5&amt=5&txAmt=0&psc=0&pdc=0&pid=june141
def payment_esewa_confirm(request):
    context={}
    rget = request.GET 

    context['action'] = "https://uat.esewa.com.np/epay/main"
    
    context['amt'] = rget.get('amt',0) #amount
    context['txAmt'] = rget.get('txAmt',0) #tax amount
    context['psc'] = rget.get('psc',0) #service charge
    context['pdc'] = rget.get('pdc',0) #delivery charge
    context['tAmt'] = rget.get('tAmt',0) #total amount

    context['scd'] = 'epay_payment'
    context['pid'] = rget.get('pid') #payment id #maybe should be unique
    
    context['su'] = 'http://kua.localtest.mew:8000/payment/payment_esewa_success' #Invalid success URL format. Missing http or https
    context['fu'] = 'http://kua.localtest.mew:8000/payment/payment_esewa_fail'


    #print(request.GET)
    print(context)
    #By default the Django template loader will look within each app for a templates folder. 
    return render(request, 'payment_esewa_confirm.html', context)


#http://kua.localtest.me:8000/payment/payment_esewa_success?oid=air7&amt=1.0&refId=00006LH
def payment_esewa_success(request):
	#esewa ko server lai sodhne
	#yo order id bhakai ho bhanera
	#tyo order id yeta db ma pani save hunu paryo
    context={}
    rget = request.GET 

    context['oid'] = rget.get('oid')
    context['amt'] = rget.get('amt')
    context['refId'] = rget.get('refId')


    print(context)
    return render(request, 'payment_esewa_success.html', context)

def payment_esewa_fail(request):
    context={}
    rget = request.GET 

    print(context)
    return render(request, 'payment_esewa_fail.html', context)