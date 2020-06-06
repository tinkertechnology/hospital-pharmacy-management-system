def payment_esewa_client_accept(request):
    context={}
    #By default the Django template loader will look within each app for a templates folder. 
    return render(request, 'payment-esewa.html', context)