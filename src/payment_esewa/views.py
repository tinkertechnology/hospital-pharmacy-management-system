from django.shortcuts import render
from carts.models import Cart
from orders.models import Order, StoreWiseOrder

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
    #
    #context['tAmt'] = rget.get('tAmt',0) #total amount
    context['tAmt'] = float( context['amt'] ) +  float( context['txAmt'] ) + float( context['psc'] ) + float( context['pdc'] )

    context['scd'] = 'epay_payment'
    context['pid'] = rget.get('pid', None)   #payment id #maybe should be unique
    if context['pid'] is None:
        context['pid'] = 'sarovara-test' + str(rget.get('cart_id')) #cart id lai token banako
    
    context['su'] = 'http://kua.localtest.mew:8000/payment/payment_esewa_success' #Invalid success URL format. Missing http or https
    context['fu'] = 'http://kua.localtest.mew:8000/payment/payment_esewa_fail'


    #print(request.GET)
    print(context)
    #By default the Django template loader will look within each app for a templates folder. 
    return render(request, 'payment_esewa_confirm.html', context)


#http://kua.localtest.me:8000/payment/payment_esewa_success?oid=air7&amt=1.0&refId=00006LH
#http://kua.localtest.mew:8000/payment/payment_esewa_success?oid=sarovara-test42&amt=76.84&refId=000071B
def payment_esewa_success(request):
	#esewa ko server lai sodhne
	#yo order id bhakai ho bhanera
	#tyo order id yeta db ma pani save hunu paryo
    context={}
    rget = request.GET 



    context['oid'] = rget.get('oid')
    context['amt'] = rget.get('amt')
    context['refId'] = rget.get('refId')

    str_cart_id = ''.join([n for n in context['oid']  if n.isdigit()])
    cart_id = int(str_cart_id)

    orders = Order.objects.filter(cart_id=cart_id) #tesai look lako
    for order in orders:
        order.is_paid = 1
        order.save()

    storeWiseOrders = StoreWiseOrder.objects.filter(cart_id=cart_id)
    for i in storeWiseOrders:
        i.is_paid = 1
        i.save()


    print(context)
    return render(request, 'payment_esewa_success.html', context)

def payment_esewa_fail(request):
    context={}
    rget = request.GET 

    print(context)
    return render(request, 'payment_esewa_fail.html', context)

def payment_esewa_app_request(request):
    context={}
    rget = request.GET 

    cart_id = rget.get('cart_id',0);
    cart = Cart.objects.get(pk=cart_id)
    context['amt'] = cart.total 
    context['cart_id'] = cart_id

    #todo:
    #pahile paid cha bhane, already paid bhannu paryo


    print(context)
    return render(request, 'payment_esewa_app.html', context)