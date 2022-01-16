from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.dispatch import receiver
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.db.models.signals import pre_save, pre_delete
from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem
from django.http import JsonResponse


class OrderListView(ListView):
    template_name = 'ordersapp/order_list.html'
    model = Order

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class CreateListView(CreateView):
    template_name = 'ordersapp/order_form.html'
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
            else:
                formset = OrderFormSet

        context_data['orderitems'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        orderitems = context_data['orderitems']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            basket_items = Basket.objects.filter(user=self.request.user)
            basket_items.delete()
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)


class UpdateListView(UpdateView):
    template_name = 'ordersapp/order_form.html'
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            formset = OrderFormSet(self.request.POST, instance=self.object)

        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context_data['orderitems'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        orderitems = context_data['orderitems']
        with transaction.atomic():

            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super().form_valid(form)

class DetailListView(DetailView):
    model = Order

class DeleteListView(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:list')

def complete(request, pk):
    order_item = Order.objects.get(pk=pk)
    order_item.status = Order.SENT_TO_PROCEED
    order_item.save()

    return HttpResponseRedirect( reverse('ordersapp:list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_on_save(sender, update_fields, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()

@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_on_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()

def get_product_price(request, pk):
    product_price = 0.0
    product = Product.objects.filter(pk=pk, is_active=True).first()
    if product:
        product_price = product.price

    return JsonResponse({'price': product_price})

