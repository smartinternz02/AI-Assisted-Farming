from django import forms

class signupform(forms.Form):
    name = forms.CharField(label="Name",max_length=50)
    email = forms.CharField(label="Email",max_length=50)
    password = forms.CharField(label="Password",max_length=50, widget=forms.PasswordInput)
    district = forms.CharField(label="District",max_length=50)
    state = forms.CharField(label="State",max_length=50)
    
class loginform(forms.Form):
    email = forms.CharField(label="Email",max_length=50)
    password = forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput)

class npk(forms.Form):
    #name = forms.CharField(label="Name",max_length=50)
    #email = forms.CharField(label="Email",max_length=50)
    #district = forms.CharField(label="District",max_length=50)
    #state = forms.CharField(label="State",max_length=50)
    crop = forms.CharField(label="Crop")
    id = forms.CharField(label="Crop Sense ID")
    n = forms.FloatField(label="Nitrogen")
    p = forms.FloatField(label="Phosphorous")
    k = forms.FloatField(label="Potassium")
    ph = forms.FloatField(label="pH")
    rainfall = forms.FloatField(label="Rainfall in mm")
    land = forms.FloatField(label="Land in Hectares")

class rev(forms.Form):
    crop_choice=[
        ("ARHAR","Arhar"),
        ("COTTON","Cotton"),
        ("GRAM","Gram"),
        ("GROUNDNUT","GroundNut"),
        ("MAIZE","Maize"),
        ("MOONG","Moong"),
        ("PADDY","Paddy"),
        ("RAPESEED AND MUSTARD","RapeSeed"),
        ("RAPESEED AND MUSTARD","Mustard"),
        ("SUGARCANE","SugarCane"),
        ("WHEAT","Wheat")
    ]    
    state_choice=[
        ("Uttar Pradesh","Uttar Pradesh"),
        ("Karnataka","Karnataka"),
        ("Gujarat","Gujarat"),
        ("Andhra Pradesh","Andhra Pradesh"),
        ("Haryana","Haryana"),
        ("Rajasthan","Rajasthan"),
        ("Madhya Pradesh","Madhya Pradesh"),
        ("Tamil Nadu","Tamil Nadu"),
        ("Bihar","Bihar"),
        ("Orissa","Orissa"),
        ("West Bengal","West Bengal"),
        ("Punjab","Punjab")
    ]
    cropchoice=forms.CharField(label="Choose Crop",widget=forms.Select(choices=crop_choice))
    statechoice=forms.CharField(label="Choose State",widget=forms.Select(choices=state_choice))