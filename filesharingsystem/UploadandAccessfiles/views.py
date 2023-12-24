from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import mimetypes
from rest_framework import viewsets
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Files
from .serializers import FilesSerializer
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class FilesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CRUD operations on Files model instances.
    """

    queryset = Files.objects.all()
    serializer_class = FilesSerializer


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_files(request):
    """
    API endpoint that returns a JSON response containing data for all Files.
    Requires token-based authentication.
    """
    data = Files.objects.all()
    serializer = FilesSerializer(data, many=True)
    return JsonResponse({"files": serializer.data})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download_file(request, pk):
    """
    API endpoint that allows downloading a specific file by its primary key.
    Requires token-based authentication.
    """
    file_instance = get_object_or_404(Files, pk=pk)
    file_path = file_instance.pdf.path
    content_type, _ = mimetypes.guess_type(file_path)
    if file_path.endswith(".docx"):
        content_type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    if not content_type:
        content_type = "application/octet-stream"
    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type=content_type)
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{file_instance.pdf.name.split("/")[-1]}"'
    return response


@api_view(["POST"])
@csrf_exempt
def user_registration(request):
    """
    API endpoint that allows user registration with a unique username and email.
    Returns a JSON response indicating the success or failure of the registration.
    """
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    print(username, password, email)
    if not username or not password or not email:
        return JsonResponse(
            {"error": "Username, password, and email are required"}, status=400
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already taken"}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email address already registered"}, status=400)

    verification_token = get_random_string(length=32)
    user = User.objects.create_user(username=username, password=password, email=email, is_active=False)

    profile = UserProfile.objects.create(user=user, verification_token=verification_token)

    verification_link = f"{settings.BASE_URL}/api/verify-email/{verification_token}/"
    send_mail(
        "Email Verification",
        f"Click the following link to verify your email: {verification_link}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    return JsonResponse({"message": "Registration successful. Please check your email for verification instructions."})

@api_view(["GET"])
@csrf_exempt
def verify_email(request, verification_token):
    """
    API endpoint that handles email verification.
    """
    user_profile = get_object_or_404(UserProfile, verification_token=verification_token)

    if user_profile.user.is_active:
        return JsonResponse({"error": "Email already verified"}, status=400)

    # Mark the user's email as verified
    user_profile.user.is_active = True
    user_profile.user.save()

    #clear the verification token after successful verification
    user_profile.verification_token = ""
    user_profile.save()

    return JsonResponse({"message": "Email verification successful"})


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    """
    API endpoint that allows user login and returns a token upon successful authentication.
    Returns a JSON response with the token or an error message for invalid credentials.
    """
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({"token": token.key})
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=400)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    API endpoint that allows user logout and deletes the authentication token.
    Requires token-based authentication.
    """
    logout(request)
    request.auth.delete()
    return JsonResponse({"message": "Logout successful"})
