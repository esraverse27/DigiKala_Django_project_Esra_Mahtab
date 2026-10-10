from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Product, Store


class UserLoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "نام کاربری یا رمز عبور نادرست است.",
        "inactive": "این حساب غیرفعال است.",
    }
    username = forms.CharField(
        label="نام کاربری",
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "username", "autofocus": True}),
    )
    password = forms.CharField(
        label="رمز عبور",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ("name", "description")
        labels = {
            "name": "نام فروشگاه",
            "description": "توضیحات فروشگاه",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "مثلاً خانومی"}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "درباره فروشگاه بنویسید"}),
        }


class AdminStoreForm(StoreForm):
    class Meta(StoreForm.Meta):
        fields = ("seller", "name", "description")
        labels = {
            **StoreForm.Meta.labels,
            "seller": "فروشنده",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "مثلاً خانومی"}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "درباره فروشگاه بنویسید"}),
        }

    seller = forms.ModelChoiceField(
        queryset=None,
        label="فروشنده",
        empty_label="انتخاب فروشنده",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import SellerProfile
        self.fields["seller"].queryset = SellerProfile.objects.exclude(store__isnull=False).select_related("user").order_by("user__username")


class SignupForm(UserCreationForm):
    role = forms.ChoiceField(
        label="نوع حساب",
        choices=(("customer", "مشتری"), ("seller", "فروشنده")),
    )
    phone = forms.CharField(label="شماره تماس", max_length=15, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)
        labels = {"username": "نام کاربری"}

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("این نام کاربری قبلاً ثبت‌نام شده است.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("رمز عبور و تکرار آن یکسان نیستند.")
            if len(password1) < 8:
                raise ValidationError("رمز عبور باید حداقل ۸ نویسه داشته باشد.")
        return password2

    def clean(self):
        # Skip UserCreationForm's default similarity/common/numeric password checks.
        cleaned_data = forms.ModelForm.clean(self)
        if cleaned_data.get("role") == "customer" and not cleaned_data.get("phone"):
            self.add_error("phone", "برای حساب مشتری واردکردن شماره تماس لازم است.")
        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "category", "price", "stock", "image")
        labels = {
            "name": "نام محصول",
            "category": "دسته‌بندی محصول",
            "price": "قیمت (تومان)",
            "stock": "موجودی محصول",
            "image": "عکس محصول",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "مثلاً کیف دستی"}),
            "price": forms.NumberInput(attrs={"min": "0", "step": "1", "placeholder": "قیمت محصول"}),
            "stock": forms.NumberInput(attrs={"min": "0", "step": "1", "placeholder": "تعداد کالای موجود"}),
        }


class AdminProductForm(ProductForm):
    store = forms.ModelChoiceField(
        queryset=None,
        label="فروشگاه",
        empty_label="انتخاب فروشگاه",
    )

    class Meta(ProductForm.Meta):
        fields = ("store", "name", "category", "price", "stock", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["store"].queryset = Store.objects.order_by("name")
