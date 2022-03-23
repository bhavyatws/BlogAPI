

from rest_framework import serializers
from home.models import Blog,User

class BlogSerializer(serializers.ModelSerializer):

    #passing extra fields in serializers
    fullname=serializers.SerializerMethodField('get_fullname_from_author')

    class Meta:
        model = Blog
        fields = ['thumbnail', 'title', 'description', 'image_url','fullname']
    
    #Writing function for fullname
    def get_fullname_from_author(self,blog):
        fullname=blog.author.first_name + ' ' + blog.author.last_name
        return fullname


class RegistrationSerializer(serializers.ModelSerializer):
    #serializers is like form here
    #write_only=True for password hidden during posting
    password2= serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['first_name','last_name','email','password','password2']
        extra_kwargs={
            'password':{'write_only':True},
            
        }

    def save(self):
        user=User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError({'password':'Password didn\'t match'})
        user.set_password(password)
        user.save()
        return user

#ProfileUpdate Serializer
class ProfilePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['pk','email','first_name','last_name']