from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Profile, Project, Task
from django.db import IntegrityError


# Create your views here.
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        confirm_password = request.POST.get("confirm_password", None)
        email = request.POST.get("email", None)
        if username is None or password is None or confirm_password is None or email is None:
            content = {
                'message': 'username or password or category_id or confirm_password  is mandatory '
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if "-" in username or "@" in username or "#" in username or "*" in username or "&" in username:
            print("hii")
            content = {
                "message": "special symbols cannot be used for usernames"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if username.isalpha() is not True or username.lstrip() == "":
            content = {
                "message": "name cannot be empty or spacing is not allowed or name cannot be number"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                print("hii")
                new_user = CustomUser.objects.create_user(username=username, password=password, email=email)
                new_user.save()
                content = {
                    'message': "new user is added",
                    'username': new_user.username,
                    "user_id": new_user.id,
                    "email": new_user.email

                }
                return Response(content, status=status.HTTP_201_CREATED)
            except IntegrityError:
                content = {
                    'message': 'user already exists'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def login(request):
    email = request.POST.get("email", None)
    password = request.POST.get("password", None)
    username = CustomUser.objects.get(email=email.lower()).username
    user = authenticate(username=username, password=password)
    if email is None or password is None:
        content = {
            "message": "user_name or password is mandatory"
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if username.lstrip() == "":
        content = {
            "message": "username cannot be empty"
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    try:
        if user is not None:
            profile = CustomUser.objects.get(id=user.id)
            content = {
                "message": "you have been successfully logged in",
                "username": profile.username,
            }
            return Response(content, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        content = {
            "message": "account is not found "
        }
        return Response(content, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user_id = request.POST.get("user_id", None)
    if user_id is None:
        content = {
            "message": "user_id is mandatory"
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    try:
        if user_id is not None:
            personal_details = Profile.objects.get(id=user_id)
            content = {
                "email": personal_details.user.email,
                "mobile": personal_details.user.mobile,
                "type_of_user": personal_details.user.type_of_user

            }
            return Response(content, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        content = {
            'message': 'user_id is invalid'
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        content = {
            'message': 'user_id should be a integer'
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def projects(request):
    members_id = request.POST.get("members_id", None)
    type_of_user = request.POST.get("type_of_user", None)
    all_projects = Project.objects.all()
    if type_of_user == "admin":
        all_projects = Project.objects.all()
    elif type_of_user == "member":
        try:
            all_projects = Project.objects.filter(members_id=members_id)
        except ValueError:
            content = {
                'message': 'members_id should be a integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    final_projects = []
    for temp_project in all_projects:
        temp = {
            'project_id': temp_project.id,
            'project_name': temp_project.name,
            'project_stage': temp_project.stage,
            'member_id': temp_project.members_id,
            'member_email': temp_project.members.user.email,
        }
        final_projects.append(temp)

    return Response(final_projects, status=status.HTTP_200_OK)
