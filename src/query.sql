Sarovara query

select 
carts_cart.id as carts_id, firstname, lastname,mobile,   
products_product.title,products_variation.title,quantity,h.id as hold_id, h.num_delta as hold_jar,
created_at,
total, debit as cash, credit
from orders_storewiseorder 
left join account_account on orders_storewiseorder.fk_auth_user_id = account_account.id 
left join carts_cart on  orders_storewiseorder.cart_id = carts_cart.id
left join carts_cartitem on carts_cartitem.cart_id = carts_cart.id
left JOIN products_variation on products_variation.id = carts_cartitem.item_id
left join products_product on products_variation.product_id = products_product.id
left join orders_usercheckout on orders_usercheckout.user_id = account_account.id
left join orders_useraddress on orders_useraddress.user_id = orders_usercheckout.user_id
left join products_uservariationquantityhistory h on h.user_id = carts_cart.user_id
where carts_cart.is_auto_order=True and carts_cart.timestamp > '2021-01-24'

aja ko sales detail
———————
select 
carts_cart.id as carts_id, firstname, lastname,mobile,   
products_product.title,products_variation.title,quantity --,h.id as hold_id, h.num_delta as hold_jar,
created_at,
total, debit as cash, credit
from orders_storewiseorder 
left join account_account on orders_storewiseorder.fk_auth_user_id = account_account.id 
left join carts_cart on  orders_storewiseorder.cart_id = carts_cart.id
left join carts_cartitem on carts_cartitem.cart_id = carts_cart.id
left JOIN products_variation on products_variation.id = carts_cartitem.item_id
left join products_product on products_variation.product_id = products_product.id
left join orders_usercheckout on orders_usercheckout.user_id = account_account.id
left join orders_useraddress on orders_useraddress.user_id = orders_usercheckout.user_id
--left join products_uservariationquantityhistory h on h.user_id = carts_cart.user_id
where carts_cart.is_auto_order=1 and carts_cart.timestamp > '2021-02-13'
--and (debit+credit) !=total

———————
jpt

select 
carts_cart.user_id, products_variation.id, products_variation.title, sum(carts_cartitem.quantity)
-- carts_cart.id as carts_id, firstname, lastname,mobile,   
-- products_product.title,products_variation.title,quantity,h.id as hold_id, h.num_delta as hold_jar,
-- created_at,
-- total, debit as cash, credit
from orders_storewiseorder 
left join account_account on orders_storewiseorder.fk_auth_user_id = account_account.id 
left join carts_cart on  orders_storewiseorder.cart_id = carts_cart.id
left join carts_cartitem on carts_cartitem.cart_id = carts_cart.id
left JOIN products_variation on products_variation.id = carts_cartitem.item_id
left join products_product on products_variation.product_id = products_product.id
left join orders_usercheckout on orders_usercheckout.user_id = account_account.id
left join orders_useraddress on orders_useraddress.user_id = orders_usercheckout.user_id
left join products_uservariationquantityhistory h on h.user_id = carts_cart.user_id
where carts_cart.is_auto_order=True
group by carts_cart.user_id, products_variation.id


keta haru lai bhatta deko query

select 
 products_variation.id, account_delivery.mobile,
products_variation.title, carts_cartitem.ordered_price as sold_at,  sum(carts_cartitem.quantity) as Quantity
-- carts_cart.id as carts_id, firstname, lastname,mobile,   
-- products_product.title,products_variation.title,quantity,h.id as hold_id, h.num_delta as hold_jar,
-- created_at,
-- total, debit as cash, credit
from orders_storewiseorder 
left join account_account on orders_storewiseorder.fk_auth_user_id = account_account.id 
left join carts_cart on  orders_storewiseorder.cart_id = carts_cart.id
left join carts_cartitem on carts_cartitem.cart_id = carts_cart.id
left JOIN products_variation on products_variation.id = carts_cartitem.item_id
left join products_product on products_variation.product_id = products_product.id
left join orders_usercheckout on orders_usercheckout.user_id = account_account.id
left join orders_useraddress on orders_useraddress.user_id = orders_usercheckout.user_id
left join products_uservariationquantityhistory h on h.user_id = carts_cart.user_id
left join account_account account_delivery on account_delivery.id = carts_cart.fk_delivery_user_id_id   
where carts_cart.is_auto_order=1
group by account_delivery.id, carts_cartitem.ordered_price, products_variation.id 


—————user ko order history———

select 
carts_cart.id as carts_id, firstname, lastname,mobile,   
products_product.title,products_variation.title,quantity --,h.id as hold_id, h.num_delta as hold_jar,
created_at,
total, debit as cash, credit
from orders_storewiseorder 
left join account_account on orders_storewiseorder.fk_auth_user_id = account_account.id 
left join carts_cart on  orders_storewiseorder.cart_id = carts_cart.id
left join carts_cartitem on carts_cartitem.cart_id = carts_cart.id
left JOIN products_variation on products_variation.id = carts_cartitem.item_id
left join products_product on products_variation.product_id = products_product.id
left join orders_usercheckout on orders_usercheckout.user_id = account_account.id
left join orders_useraddress on orders_useraddress.user_id = orders_usercheckout.user_id
--left join products_uservariationquantityhistory h on h.user_id = carts_cart.user_id
where carts_cart.is_auto_order=1 and mobile='9869875409'
--and (debit+credit) !=total



———— check sales thik xa ke chaina ——— 
select 
carts_cart.id as carts_id, firstname, lastname,mobile,   
products_product.title,products_variation.title,quantity --,h.id as hold_id, h.num_delta as hold_jar,
created_at,
total, debit as cash, credit
from orders_storewiseorder 
left join account_account on orders_storewiseorder.fk_auth_user_id = account_account.id 
left join carts_cart on  orders_storewiseorder.cart_id = carts_cart.id
left join carts_cartitem on carts_cartitem.cart_id = carts_cart.id
left JOIN products_variation on products_variation.id = carts_cartitem.item_id
left join products_product on products_variation.product_id = products_product.id
left join orders_usercheckout on orders_usercheckout.user_id = account_account.id
left join orders_useraddress on orders_useraddress.user_id = orders_usercheckout.user_id
--left join products_uservariationquantityhistory h on h.user_id = carts_cart.user_id
where carts_cart.is_auto_order=1 and carts_cart.timestamp > '2021-02-13'
and (debit+credit) !=total


