from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     context = {
#         'object_list': ShopUser.objects.all().order_by('-is_active')
#     }
#     return render(request, 'adminapp/users_list.html', context)

class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'


    @method_decorator (user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)

@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()
    context = {
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    # ShopUserAdminEditForm
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)
    context = {
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        current_user.is_active = False
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))
    context = {
        'object': current_user
    }
    return render(request, 'adminapp/user_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'object_list': ProductCategory.objects.all()
    }

    return render(request, 'adminapp/categoties_list.html', context)

# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         form = ProductCategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         form = ProductCategoryForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'adminapp/category_form.html', context)

class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')



# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#         category_item = get_object_or_404(ProductCategory, pk=pk)
#         if request.method == 'POST':
#             form = ProductCategoryForm(request.POST, instance=category_item)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect(reverse('adminapp:categories'))
#         else:
#             form = ProductCategoryForm(instance=category_item)
#         context = {
#             'form': form
#         }
#         return render(request, 'adminapp/category_form.html', context)

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('adminapp:categories'))
#     context = {
#         'object': category
#     }
#     return render(request, 'adminapp/category_delete.html', context)

class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')


    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)





@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    context = {
        'object_list': Product.objects.filter(category__pk=pk),
        'category': category_item
    }

    return render(request, 'adminapp/products_list.html', context)


class PProductEditForm:
    pass


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_item = product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category.pk]))
#     else:
#         product_form = ProductForm()
#     context = {
#         'form': product_form,
#         'category': category_item
#     }
#
#     return render(request, 'adminapp/products_form.html', context)

class ProductCreateView(CreateView):
    model = products
    template_name = 'adminapp/products_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('adminapp:categories')

    def get_success_url(self):
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        return reverse('adminapp:products', args=[category_item.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        context_data['category'] = category_item
        return context_data



@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):

    product_item = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product_item)
        if product_form.is_valid():
            product_item = product_form.save()
            return HttpResponseRedirect(reverse('adminapp:product', args=[product_item.category.pk]))
    else:
        product_form = ProductForm(instance=product_item)
    context = {
        'form': product_form,
        'category': product_item.category
    }

    return render(request, 'adminapp/products_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    product_item = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_item.is_active = False
        product_item.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category.pk]))
    context = {
        'object': product_item
    }
    return render(request, 'adminapp/user_delete.html', context)

# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     context = {
#         'object': product_item
#     }
#
#     return render(request, 'adminapp/products_read.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/products_read.html'
