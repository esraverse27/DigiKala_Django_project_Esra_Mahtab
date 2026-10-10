# digikala_Esra-Mahtab

##accounts app

###models
-here we have a class(model) of users wich inheritates AbstractUser

-we have a class for managing users wich inheritates UserManager. we overwrited functions of creating user and superuser to use phone as username.


###views and forms
_in forms.py we created forms of login and registration. we imported theme in views and sent theme as a dictionary to the templates of login and registration. at `form = registration_form` we define the variable and in `render(,,{'form',form})` string 'form' in html stands for the form we have defined. it lets us make intraction between front and backend.

-in views functions basically get request as input, wich are sent by urls from client to server. they contain a lot of data about the request they send. and the type af it, for example POST or GET.

_in login and signin methods, we get two types of functions according to the type of reqest. if the request is containing secret data like password and actually when the user registered valid data and they are being sent to the server, the method is post. in this case, we ridirect user to another page, for example home. but if the method is get, we show him the form page. this should happen both when he clicks on it for the first time, and when reloading after entering invalid input.
 
