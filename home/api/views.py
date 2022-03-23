
from http import server
from random import seed
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#For authentication and permission
from home.models import Blog,User
from home.api.serializers import BlogSerializer, RegistrationSerializer,ProfilePropertySerializer

#For pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

#For Searching i.e Filtering and Ordering
from rest_framework.filters import SearchFilter,OrderingFilter


@api_view(['GET',])

def api_blog_view(request):
  
    blog=Blog.objects.all()
    
    if request.method == "GET":
        serializer=BlogSerializer(blog,many=True)
    
        return Response(serializer.data)
    
    return Response(status=status.HTTP_204_NO_CONTENT)
    
    

@api_view(['GET',])
def api_blog_detail_view(request,slug):
    try:
        blog=Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == "GET":
        serializer=BlogSerializer(blog)
        return Response(serializer.data)


@api_view(['PUT',])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated,])
def api_blog_update_view(request,slug):
    try:
        blog=Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    #checking the author post and author only can update
    user=request.user
    if blog.author!=user:
        return Response({'data':'You don"t have permission to update others blog'})

    if request.method == "PUT":
        serializer=BlogSerializer(blog,data=request.data)
        data = {}#data is context
        if serializer.is_valid():#its equivalent to form.is_valid()
            serializer.save()
            data["success"]="Update Successfull"
            return Response(data=data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE',])
# @authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
def api_blog_delete_view(request,slug):
    try:
        blog=Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
     #checking the author post and author only can delete that
    user=request.user
    if blog.author!=user:
        return Response({'data':'You don"t have permission to update others blog'})

    if request.method == "DELETE":
        operation=blog.delete()
        
        data = {}#data is context
        if operation:#its equivalent to form.is_valid()
           
            data["success"]="Delete Successfull"
        else:
            data["failure"]="Delete Failed"

        return Response(data=data)
        
       
@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def api_blog_create_view(request):
    
    # user=User.objects.get(pk=1)#this is hard code 
    user=request.user#as is IsAuthenticated is here so that we can currently login user
   
    blog=Blog(author=user)
    
    
    if request.method == "POST":
        serializer=BlogSerializer(blog,data=request.data)
        
     
        if serializer.is_valid():#its equivalent to form.is_valid()
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
           

        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def registration_api_view(request):
    
    if request.method == "POST":
        serializer=RegistrationSerializer(data=request.data)
        data={}
     
        if serializer.is_valid():#its equivalent to form.is_valid()
            user=serializer.save()
            data['response']='Successfully registered a new user'
            data['email']=user.email
            data['first name']=user.first_name
            data['last name']=user.last_name
            token=Token.objects.get(user=user).key
            # print("Token Key",token.key)
            data['Token']=token
        else:
            data=serializer.errors
        return Response(data)
           

        # return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

#ClassBased Pagination View
class PaginationListView(ListAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    authentication_classes=(TokenAuthentication,)#if no comma then error will arise
    permission_classes=(IsAuthenticated,)#if no comma then error will arise
    pagination_class= PageNumberPagination
    #For searching 
    filter_backends=(SearchFilter,OrderingFilter)
    search_fields=['title','description','author__email',]


#ProfileProperty
@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def profile_property_view(request):
    try:
        profile=request.user
    except profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    
    
    if request.method == "GET":
        serializer=ProfilePropertySerializer(profile)
    
        return Response(serializer.data)
    
    return Response(status=status.HTTP_204_NO_CONTENT)

#ProfileUpdate
@api_view(['PUT',])
@permission_classes([IsAuthenticated,])
def profile_update_view(request):
    try:
        profile=request.user
    except profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer=ProfilePropertySerializer(profile,data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data['response']="Profile Updated Successfully"
            return Response(data=data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
       
