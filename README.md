# digikala_Esra-Mahtab


how does our code work?

## shop.admin
at first class SuperuserOnlyAdmin limitates permissions of user which are not superuser.
then we register model datas to let superusers manage theme at site.


## accounts app

### models
- here we have a class(model) of users wich inheritates AbstractUser
- we have a class for managing users wich inheritates UserManager. we overwrode functions of creating user and superuser to use phone as username.

### views and forms
- in forms.py we created forms of login and registration. we imported theme in views and sent theme as a dictionary to the templates of login and registration. at `form = registration_form` we define the variables and in `render(,,{'form',form})` string 'form' in html stands for the form we have defined and its value is our form. it lets us make intraction between front and backend.

- in views functions basically get request as input, wich are sent by urls from client to server. they contain a lot of data about the request they send. and the type of it is somtimes POST and sometimes GET.

- in login and signin methods, we get two types of functions according to the type of reqest. if the request is containing secret data like password and actually when the user registered valid data and they are being sent to the server, the method is post, because we don't want the data to be shown in url. in this case, we save his datas and ridirect him to the home page. but if the method is get, we show him the form page. this should happen both when he clicks on it for the first time, and when reloading after entering invalid input.
 

in method login_viwe instead of all this:
```
if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
```
we said
```
if request.user.is_authenticated:
        return redirect("home")
    form = UserLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")
```
if user is not logged in we give user's information by 'form.get_user()'

### permissions
* when we start a method's name with _ we are informing that this method is only used inside the code 

- we have _require_admin _require_seller and _require_customer. their task is to find wanted user from database.
`SellerProfile.objects.filter(user=request.user)`
SellerProfile is the the model which refers to the database. bjects.filter says filter the datas in it by attribute user. and return it if the value user equals with 
user.request, given from the clients request.


## shop
- the main code is written here. 
- in models.py we created databases for stores, products, customers and sellers.

the MVT engineering means that we create classes in models. the ORM of django makes database of project using our models.
in views we write basic queries. for example we give datas from the classes made in models or filter datas by their attribute and make a list of wanted datas.here we write the logic of our code. sometimes we use built in functions for validation and other things. for example:
`products=Product.objects.all()`
then we send theme to templates and in templates we say do something with theme. for example:
```
{% for product in products %}
    {{ product.name }}
{% endfor %}
```


### home
- `query = request.GET.get("q", "").strip()` gets value of q=...  part of url and if there isn't this part, it returns null.
- here we initialize datas we get from request and show theme in home.html

in query functions,  __ sometimes means that we are getting an attribute of object. for example: `.filter(product__category=selected_category)` here we get category of the product and check it.

 Prefetch is a django built in class which helps us optimize our queries. for example in: `Prefetch("product_set", queryset=Product.objects.filter(...), to_attr="panel_products")` , we are creating an object of the class, and overriding something about the datas. here it says get filtered datas and add theme to an attribute named 'panel_products'.

### _catalog_panel
* how does it work?
- it's for managing the store in two cases, for seller and the manager
- if method of request is post, for each kind of action we define the metod. we have save_store and add_product in cases that admin_panel given in method is true or false. 
- then we returened it in manager_panel and seller_panel methods. in manager panel, admin_pannel is true and in seller_panel it's false.
- it validates needed datas and renders 'manager_panel.html'

### manager_edit_product and manager_delete_product
`<a class="..." href="{% url 'manager_edit_product' product.id %}">ویرایش</a>` this part in manager_panel.html, refers to:
 `path('manager/products/<int:product_id>/edit/', manager_edit_product, name='manager_edit_product')` in shop.urls,
 and this url refers to manager_edit_product(request, product_id) method in shop.views . product_id is sent from user in template to view the function and here we can use it.
 if we call the method for the first time with method get, it renders the related page and gives it wanted dictionary. and with method post it ridirects.

 ### customer_panel seller_panel and manager_panel
 they use functions defined in accounts to authenticate user and his role.
 ```def _require_seller(request):
    if not SellerProfile.objects.filter(user=request.user).exists():
        raise PermissionDenied
``` 
in accounts.permission we have such functions for authenticating user.


## cart

### models
- we have cart item that gets a product and a quantity for it
it has a foreign key to cart and each cart item is related to a special cart

- we have cart wich saves the items of each user, and each of theme is related to one user. so it uses one to one field.

### views and templates

`<a class="..." href="{% url 'cart' %}">سبد خرید</a>`in base.html refers to `path('my_cart/', cart, name='cart'),` and then we have cart method which defines the customer and his items. then through `return render(request, "cart.html", {"cart_items": items, "total": total})` we have:

```
{% for item in cart_items %}
    <tr>
        <td class="cart-product-name">{{ item.product.name }}</td>
        <td>{{ item.product.store.name }}</td>
        <td>{{ item.product.price|floatformat:"-2" }} تومان</td>
        <td>
            <form class="cart-quantity-form" method="post" action="{% url 'update_cart_item' item.id %}">
                {% csrf_token %}
                <input type="number" name="quantity" min="1" max="999" value="{{ item.quantity }}" aria-label="تعداد {{ item.product.name }}">
                <button type="submit" class="cart-update-button">ثبت</button>
            </form>
        </td>
        <td>{{ item.line_total|floatformat:"-2" }} تومان</td>
        <td>
            <form method="post" action="{% url 'remove_from_cart' item.id %}">
                {% csrf_token %}
                <button type="submit" class="delete-cart-item">حذف</button>
            </form>
        </td>
    </tr>
{% endfor %}
```
here the form action is a url we have in cart.urls . for example `<form method="post" action="{% url 'remove_from_cart' item.id %}">` sends the data to the method remove_from_cart(request, item_id) and we can process it there.


## order

order and order item is defined completely like cart and cart item. we create an order and we submit the informaton about it, so the date created and total prise will not change as we do in cart.






