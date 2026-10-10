# digikala_Esra-Mahtab


## shop.admin
- at first class SuperuserOnlyAdmin limitates permissions of user which are not superuser.
- then we register model datas to let superusers manage theme at site.


## accounts app

### models
- here we have a class(model) of users wich inheritates AbstractUser
- we have a class for managing users wich inheritates UserManager. we overwrited functions of creating user and superuser to use phone as username.

### views and forms
_ in forms.py we created forms of login and registration. we imported theme in views and sent theme as a dictionary to the templates of login and registration. at `form = registration_form` we define the variables and in `render(,,{'form',form})` string 'form' in html stands for the form we have defined and its value is our form. it lets us make intraction between front and backend.

- in views functions basically get request as input, wich are sent by urls from client to server. they contain a lot of data about the request they send. and the type af it is somtimes POST and sometimes GET.

_ in login and signin methods, we get two types of functions according to the type of reqest. if the request is containing secret data like password and actually when the user registered valid data and they are being sent to the server, the method is post. in this case, we save his datas and ridirect him to home page. but if the method is get, we show him the form page. this should happen both when he clicks on it for the first time, and when reloading after entering invalid input.
 

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
* when we start a method's name with _ we inform that this method is only used inside the code 

- we have _require_admin _require_seller and _require_customer. their task is to find wanted user from database.
`SellerProfile.objects.filter(user=request.user)`
SellerProfile is the database. .bjects.filter says filter the datas in it by attribute user. and return it if the value user equals with user.request, given from the clients request.


## shop
- the main code is written here. 
- in models.py we created databases for stores, products, customers and sellers.

the MVT engineering means that we create database in models. 
in views we write basic queries. for example we give datas from the classes made in models or filter datas by their attribute and make a list of wanted datas.sometimes we use built in functions for validation and other things. for example:
`products=Product.objects.all()`

then we send theme to templates and in templates we say do something with theme. for example:
```
{% for product in products %}
    {{ product.name }}
{% endfor %}
```


