from scipy.spatial.distance import cosine
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Item, OrderItem, Order, Comment
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from core.models import *
from django.db import transaction
# Create your views here.
def White_View(request):
    return redirect('core:home')
def Home_View(request):
    return render(request, 'index.html')

def Shop_View(request):
    products = Item.objects.all()
    return render(request, 'shop.html', {'products' : products   })
def Thank_You(request):
    return render(request, 'thankyou.html')

def products(request):
    context = {
        'recommended_items': product_id,
        'items': Item.objects.all()
    }
    product_id = recommendation(request.user.id)
    item = Item(product_id)
    return render(request, 'products.html', context)

@login_required
def cart(request):
    """
    Display the user's shopping cart.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders the 'cart.html' template with the items in the user's cart.

    Role of the class:
    This function is responsible for displaying the contents of the user's shopping cart. 
    It ensures that only authenticated users can access the cart by using the @login_required
    decorator. It retrieves the product IDs associated with the current user from the Cart model, 
    then fetches the corresponding items from the Item model. Finally, it renders the 'cart.html' 
    template with the retrieved items for display.
    """
    product_ids = Cart.objects.filter(user_id=request.user.id).values_list('product_id', flat=True)
    items = Item.objects.filter(product_id__in=product_ids)
    return render(request, 'cart.html',{'items' : items})


@transaction.atomic
@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the user's shopping cart.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - product_id (int): The ID of the product to add to the cart.

    Returns:
    - HttpResponseRedirect: Redirects to the 'cart' view after adding the product to the cart.

    Role of the class:
    This function handles the addition of a product to the user's shopping cart. It takes 
    the product ID and quantity as input from the request POST data. It first retrieves 
    the product object using the provided product ID. Then, it attempts to find an existing 
    cart item for the user and the specified product. If a cart item already exists, it 
    increments the quantity by one. If not, it creates a new cart item with the specified 
    quantity. After updating or creating the cart item, it redirects the user to the 'cart' view.
    """
    product= get_object_or_404(Item, pk = product_id)
    quantity = int(request.POST['quantity'])
    cart = Cart.objects.filter(product_id=product_id, user_id=request.user.id).first()
    if cart:
        cart.quantity += int(1)
        cart.save()
    else:
        cart = Cart.objects.create(user_id=request.user.id, product_id=product_id, quantity=quantity)

    return redirect('core:cart')

@login_required
def remove_from_cart(request, cart_id):
    """
    Removes a cart item from the user's cart.

    Retrieves the cart item object based on the provided cart item ID and user.
    Deletes the cart item.
    Finally, redirects the user to the cart page.

    Args:
        request (HttpRequest): The HTTP request object.
        cart_item_id (int): The ID of the cart item to be removed.

    Returns:
        HttpResponseRedirect: A redirect response to the cart page.
    """
    cart= get_object_or_404(Cart, pk = cart_id, user = request.user)
    cart.delete()
    return redirect('core:cart')

@login_required
def checkout(request):
    """
    Display the checkout page with items in the user's shopping cart.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders the 'checkout.html' template with the items in the user's cart.

    Role of the class:
    This function is responsible for displaying the checkout page with the items currently 
    in the user's shopping cart. It retrieves the product IDs associated with the current 
    user from the Cart model and then fetches the corresponding items from the Item model. 
    Finally, it renders the 'checkout.html' template with the retrieved items for display 
    during the checkout process.
    """
    product_ids = Cart.objects.filter(user_id=request.user.id).values_list('product_id', flat=True)
    items = Item.objects.filter(product_id__in=product_ids)
    
    return render(request,'checkout.html',{'items' : items})
    
@login_required
def placeorder(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    
    cart_items = Cart.objects.filter(user_id=request.user.id)
    for cart_item in cart_items:
        cart = Item.objects.filter(product_id=cart_item.product_id).first()
        order_detail = OrderDetail.objects.create(
            product_id=cart_item.product_id,
            user_id=cart_item.user_id,
            quantity=cart_item.quantity,
            firstname = firstname,
            lasttname = lastname,
            email = email,
            phone = phone,
            address = address,
            price = cart_item.quantity * cart.product_price_new)
    return redirect('core: home/')

def productdetail(request, product_id):
    product = get_object_or_404(Item, product_id=product_id)
    products = Item.objects.all()
    comments = Comment.objects.filter(product_id=product_id)
    comment_data = []
    for comment in comments:
        comment_data.append({
            'comment' : comment.comment,
            'date' : comment.date,
        })
    if request.user.is_authenticated:
        product_recommend = recommendation(request.user.id)
        print(product_recommend)
        return render(request, 'detail.html', {'product' : product, 'products' : products, 'comments' : comment_data, 'product_recommend' : product_recommend})
    else:
        return render(request, 'detail.html', {'product' : product, 'products' : products, 'comments' : comment_data, 'product_recommend' : products})

@login_required
def vote(request, vote, product_id):
    """
    Register a user's vote for a product.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - vote (int): The user's vote for the product.
    - product_id (int): The ID of the product being voted on.

    Returns:
    - HttpResponse: Renders the 'thankyou.html' template after registering the vote.

    Role of the class:
    This function handles the process of registering a user's vote for a particular product. 
    It takes the user's vote (either upvote or downvote), along with the product ID, as input. 
    It retrieves the product object using the provided product ID. If the request method is GET, 
    it creates a new Voting object to register the user's vote for the product. Finally, it 
    renders the 'thankyou.html' template to acknowledge the successful registration of the vote.
    """
    product = get_object_or_404(Item, product_id=product_id)
    if request.method == 'GET': 
        rate = Voting.objects.create(
            user = request.user,
            product = product,
            vote = vote
        )
    return render(request, 'thankyou.html')

@login_required
def addcomment(request, product_id):
    """
    Add a comment to a product.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - product_id (int): The ID of the product to add the comment to.

    Returns:
    - HttpResponseRedirect: Redirects to the 'home/' page after adding the comment.

    Role of the class:
    This function handles the process of adding a comment to a product. It takes the product 
    ID as input and retrieves the corresponding product object. It also retrieves the comment 
    text from the request POST data. Then, it creates a new Comment object associated with 
    the product, user, and comment text. Finally, it redirects the user to the 'home/' page 
    after successfully adding the comment.
    """
    user = request.user
    product = get_object_or_404(Item, product_id=product_id)
    comment_get = request.POST.get('comment')
    Comment.objects.create(
        product = product,
        user= user,
        comment = comment_get,
        date = date.today()
    )
    return redirect('home/')
    
@login_required
def addfavorite(request, product_id):
    """
    Add or remove a product from the user's favorites list.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - product_id (int): The ID of the product to add/remove from favorites.

    Returns:
    - HttpResponseRedirect: Redirects to the 'favorite' view after adding/removing the product.

    Role of the class:
    This function allows users to add or remove a product from their favorites list. It takes 
    the product ID as input and retrieves the corresponding product object. Then, it checks 
    if the product is already in the user's favorites list. If it is, it removes the product 
    from favorites. If not, it adds the product to favorites. Finally, it redirects the user 
    to the 'favorite' view to display the updated favorites list.
    """
    product = Item.objects.get(product_id=product_id)
    user = request.user
    favorite = Favorite.objects.filter(product_id = product_id, user_id = request.user.id)
    if(favorite.exists()):
        favorite.delete()
    else:
        Favorite.objects.create(
            product = product,
            user = user
        )
    return redirect('core:favorite')

@login_required
def favorite(request):
    """
    Displays the user's favorite products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response rendering the 'favorite' page.
    """
    user = request.user
    favorite_list = Favorite.objects.filter(user_id = request.user.id)
    if favorite_list.exists():
        products = Item.objects.filter(product_id__in=favorite_list.values('product_id'))
        return render(request, 'favorite.html', {'products' : products})
    else:
        message = "You don't have any favorites yet."
        return render(request, 'favorite.html', {'message': message})

def Sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home/')
        else:
            error_message = form.errors
            print(error_message)
            render(request, 'signup.html', {'error_message': error_message})
    else:
        form = UserCreationForm()
    return render(request,'signup.html', {'form':form})


def Log_in(request):
    """
    Handle user login.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: If the request method is POST and user authentication is successful, 
      it redirects to '/home/'. If authentication fails or request method is not POST, 
      renders the login page with appropriate error message.

    Role of the class:
    This function handles the login process for users. It takes a request object as input,
    which contains user login credentials. If the request method is POST, it attempts to 
    authenticate the user using the provided credentials. If authentication is successful, 
    it logs the user in and redirects to the home page. If authentication fails or the 
    request method is not POST, it renders the login page again with an error message.
    """
    if request.method == 'POST':
        # Get user from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            error_message = form.errors
            print(error_message)
            return render(request, 'login.html', {'error_message' : error_message})
    else:
        form = UserCreationForm()
    return render(request, 'login.html', {'form':form})

def recommendation(user_id):
    users = User.objects.exclude(id=user_id)
    items = Item.objects.all()
    
    # Create a matrix to store user-item ratings
    ratings_matrix = np.zeros((len(users), len(items)))

    # Populate the ratings matrix
    for i, user in enumerate(users):
        for j, item in enumerate(items):
            try:
                rating = Voting.objects.get(user=user, product=item).vote
                ratings_matrix[i, j] = rating
            except Voting.DoesNotExist:
                pass

    # Calculate similarity between users
    user_similarities = np.zeros(len(users))
    user_ratings = ratings_matrix[user_id]
    for i, ratings in enumerate(ratings_matrix):
        user_similarities[i] = 1 - cosine(user_ratings, ratings)

    # Sort users by similarity
    sorted_users = np.argsort(-user_similarities)

    # Get top N similar users
    top_similar_users = sorted_users[:10]

    # Collect items rated by top similar users but not rated by the target user
    recommendations = set()
    for user_index in top_similar_users:
        for item_index, rating in enumerate(ratings_matrix[user_index]):
            if rating > 0 and user_ratings[item_index] == 0:
                recommendations.add(items[item_index])   

    return recommendations


class CustomUserLoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': TextInput(attrs={'placeholder': 'Username', 'required' : True}),
            'password': PasswordInput(attrs={'placeholder': 'password', 'required': True})
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': TextInput(attrs={'placeholder': "Username", 'required': True}),
            'email': TextInput(attrs={'placeholder': "info@example.com", 'required': True}),
            'password1': PasswordInput(attrs={'placeholder': "password1", 'required': True}),
            'password1': PasswordInput(attrs={'placeholder': "password2", 'required': True})
        }

class CustomUserLoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': TextInput(attrs={'placeholder': "Username", 'required': True}),
            'password': TextInput(attrs={'placeholder': "password", 'required': True})
        }
