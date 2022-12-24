from django.shortcuts import redirect, render,get_object_or_404
from requests import request
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    products = Product.objects.all
    return render(request,'Shop/home.html',{'products':products})



def SellerCenter(request):
    print(request.user.id)

    #(user__id = request.user.id)
    try:
        seller = Seller.objects.get(user__id = request.user.id )
    except:
        messages.error(request, "Create your Seller Profile")
        products =  Product.objects.filter(seller__id = None)
    else:
        products =  Product.objects.filter(seller__id = seller.pk)
    return render(request,'Shop/sale-home.html',{'products':products})

def SellerOrders(request):
    
    seller = Seller.objects.get(user__id = request.user.id)
    orders = OrderProduct.objects.filter(product__seller = seller)
    return render(request,'Shop/seller-orders.html',{'orders':orders})



def CreateProduct(request):
    seller = Seller.objects.get(user__id = request.user.id)
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sale_center')
            
    form = ProductForm()
    return render(request,'Shop/create-product.html',{'form':form,'seller':seller})


def EditProduct(request,pk):
    seller = Seller.objects.get(user__id = request.user.id)
    product =  Product.objects.get(id = pk)
    if request.method == 'POST':
        form = ProductForm(instance=product, data=request.POST,files = request.FILES)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('sale_center')

    else:
        form = ProductForm(instance=product)
    return render(request,'Shop/edit-product.html',{'form':form,'product':product,'seller':seller})
  

def DeleteProduct(request,pk):
    product =  Product.objects.get(id = pk)
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            product.delete()
            return redirect('sale_center')
    else:
        form = ConfirmForm()
    return render(request,'Shop/delete-product.html',{'form':form,'product':product,})


def SellerProfile(request):
    try:
        seller = Seller.objects.get(user__id = request.user.id)
    except:
        seller = None
    else:
        seller = Seller.objects.get(user__id = request.user.id)
    if request.method == 'POST':
        form  = SellerProfileForm(instance=seller,data=request.POST)
        if form.is_valid():
           form.save()
           return redirect('sale_center')
    else:
       form = SellerProfileForm(instance=seller)

    return render(request,'Shop/seller-profile.html',{'form':form,'seller':seller})

from django.contrib.auth import logout
def SellerLogout(request):
    logout(request)
    return redirect('seller_login')

def CustomerLogout(request):
    logout(request)
    return redirect('customer_login')

def CustomerSignUp(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            authenticate(email = email, password = raw_password)
            login(request,user)
            return redirect('home')
    else:
        form = CustomerCreationForm()
    return render(request,'Shop/signup.html',{'form':form})


def SellerSignUp(request):
    if request.method == 'POST':
        form = SellerCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            authenticate(email = email,password = raw_password)
            login(request,user)
            return redirect('sale_center')
    else:
        form = SellerCreationForm()
    return render(request,'Shop/seller_signup.html',{'form':form})


def ProductDetail(request,pk,category):
    product = Product.objects.get(id =pk)
    num = (product.discount_price / product.price) *100
    discount_rate = round(num,2)
    return render(request,'Shop/product-detail.html',{'product':product,'discount_rate':discount_rate})



class OrderSummaryView(LoginRequiredMixin, View):
    login_url = 'customer_login'
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            
            context = {
                'object': order
            }
            return render(self.request, 'Shop/product-cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")


from django.contrib.auth.views import LoginView
from django.urls import is_valid_path, reverse_lazy

class CustomerLogin(LoginView):
    template_name = 'Shop/customer-login.html'
    form_class = CustomerLoginForm
   

   
class SellerLogin(LoginView):
    template_name = 'Shop/customer-login.html'
    form_class = SellerLoginForm
    next_page = 'sale_center'
   
    
   

    

@login_required(login_url = 'customer_login')
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_item,a = OrderProduct.objects.get_or_create(
        product = item,
        user = request.user,
        ordered = False
    )
    print(a)
    print(order_item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    #print(order_qs)
    #print(order_qs.exists())
    if order_qs.exists():#check if order exists
        #print(order_qs[0])
        order = order_qs[0]#grab user who made the order

        if order.product.filter(product__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("order-summary")
        else:
            order.product.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.product.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("order-summary")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__pk=item.pk).exists():
            order_item = OrderProduct.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \""+order_item.product.name+"\" remove from your cart")
            return redirect("order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("product", pk=pk)
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("product", pk = pk)


@login_required
def reduce_quantity_item(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__pk=item.pk).exists() :
            order_item = OrderProduct.objects.filter(
                product = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                #order_item.delete()
                order_item.quantity = 1
            messages.info(request, "Item quantity was updated")
            return redirect("order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("order-summary")
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("order-summary")





class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }
      
        return render(self.request, 'Shop/check-out.html', context)
    
    def post(self,*args,**kwargs):
        print(self.request.POST)
        form = CheckoutForm(self.request.POST or None)
  
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                payment_option = form.cleaned_data.get('payment_option')
                order.save()
                if payment_option == 'P':
                    return redirect('payment')
                
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("order-summary")
        #return redirect('home')



class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = int(order.get_total_price() * 100)  #cents
        context = {
            'order': order,
            'amount':amount,
        }
        return render(self.request, "Shop/payment.html", context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        payment = Payment()
        payment.user = self.request.user
        payment.amount = order.get_total_price()
        payment.save()
      
        # assign payment to order
        print('before',order.ordered)
        order.ordered = True
        order.payment = payment
        print('After',order.ordered)
        order.save()

        return redirect('home')
        

       

        

        
