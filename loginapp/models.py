
import re
from django.db import models 
import bcrypt

class Usermanager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex =re.compile(r'^[a-zA-Z0-9.+_-]')
        special_symbols = ['$','@','#','%','^','&']

        if len(postData['name']) < 2:
            errors["name"] = "user first_name should be at least 2characters"
        if len(postData['Lname']) < 2:
            errors["Lname"] = "userL_name should be at least 2characters"
        if len(postData['password']) < 8:
            errors["password"] = "user password should be at least 8characters"
        if len(postData['cpassword']) < 2:
            errors["cpassword"] = "user cpassword should be at least 8characters"
        if postData['cpassword']!=postData['password']:
            errors["cpassword"] ='password not matches'
        
        if not EMAIL_REGEX.match(postData['Email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if not any(characters.isupper() for characters in postData['password']):
            errors['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            errors['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            errors['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            errors['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        return errors

class User (models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    Email=models.CharField(max_length=255)
    password=models.TextField(max_length=255)
    cpassword=models.IntegerField(max_length=255)
    objects=Usermanager()

def create_user(request):
    first_name=request.POST['name']
    last_name=request.POST['Lname']
    Email=request.POST['Email']
    password=request.POST['password']
    cpassword=request.POST['cpassword']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
    if (cpassword == password):
        return User.objects.create(first_name = first_name , last_name = last_name, Email = Email , password = pw_hash )
    

def login(request):
    user = User.objects.filter(Email = request.POST['Email'])
    if user:
        loged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loged_user.password.encode()):
            request.session['userid'] = loged_user.id
            return True

def get_login(id):
    return User.objects.get(id=id)
