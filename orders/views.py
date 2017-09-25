from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from orders.forms import CheckoutForm, ProductInOrder, Order
from orders.models import ProductInBasket


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get('product_id')
    nmb = data.get('nmb')
    is_delete = data.get('is_delete')

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key,
                                                                     product_id=product_id, is_active=True,
                                                                     defaults={'nmb':nmb})
        if not created:
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    product_total_nmb = products_in_basket.count()
    return_dict['product_total_nmb'] = product_total_nmb
    return_dict['products'] = list()

    for i in products_in_basket:
        product_dict = dict()
        product_dict['id'] = i.id
        product_dict['name'] = i.product.name
        product_dict['price_per_item'] = i.price_per_item
        product_dict['nmb'] = i.nmb
        return_dict['products'].append(product_dict)

    return JsonResponse(return_dict)

def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    form = CheckoutForm(request.POST or None)
    if form.is_valid():
        data = request.POST
        name = data.get('name')
        phone = data['phone']
        user = User.objects.get_or_create(username=phone, defaults={'first_name': name})

        order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)
        for name, value in data.items():
            if name.startswith("product_in_basket_"):
                id = name.split('product_in_basket_')[1]
                product = ProductInBasket.objects.get(id=id)

                product.nmb = int(value)
                product.save(force_update=True)

                ProductInOrder.objects.create(product=product.product, nmb=product.nmb,
                                              price_per_item=product.price_per_item,
                                              total_price=product.total_price,
                                              order=order)


    return render(request, 'checkout.html', locals())