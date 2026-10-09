from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from .models import Product, Store


class UserLoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "نام کاربری یا رمز عبور نادرست است.",
        "inactive": "این حساب غیرفعال است.",
    }
    username = forms.CharField(
        label="شماره تلفن",
        max_length=11,
        widget=forms.TextInput(attrs={"autocomplete": "tel", "autofocus": True}),
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
        self.fields["seller"].queryset = SellerProfile.objects.exclude(store__isnull=False).select_related("user").order_by("user__phone")


class SignupForm(UserCreationForm):
    role = forms.ChoiceField(
        label="نوع حساب",
        choices=(("customer", "مشتری"), ("seller", "فروشنده")),
    )
    phone = forms.CharField(label="شماره تماس", max_length=11, required=True)
    first_name = forms.CharField(label="نام", max_length=100, required=False)
    last_name = forms.CharField(label="نام خانوادگی", max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("first_name", "last_name", "phone")
        labels = {"phone": "شماره تماس", "first_name": "نام", "last_name": "نام خانوادگی"}

    def clean(self):
        cleaned_data = super().clean()
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
