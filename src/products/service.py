from django.conf import settings	
from store.models import Store, StoreUser
def getUserStoreService(user_id):
    settings.DLFPRINT()
    # queryset = Product.objects.all() ##debug if not working location
    # return queryset
    users_store = None #user ko store (instance of Store)
    main_users_store = Store.objects.filter(fk_user_id=user_id).first() #company / depo ko main user #(instance Store)

    #todo: make service for getting store of user, isUserStore, isUserCustomer
    if main_users_store is not None:
        users_store = main_users_store
    else:
        storeUser = StoreUser.objects.filter(fk_user_id=user_id).first()
        if(storeUser is not None):
            users_store = storeUser.fk_store
    return users_store
    