from rest_framework.decorators import api_view,action
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import  PeopleSerializer,ColorSerializer,LoginSerializer,RegisterSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import viewsets
from .models import Persons
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from rest_framework_simplejwt.tokens import RefreshToken
@api_view(['GET','POST'])
def index(request):
    if request.method == 'GET':
        courses = {
            'course_name': "Python",
            'learn': ["Django", "Flask"],
            "platform": "youtube"
        }
        return Response(courses)
    elif request.method == 'POST':
        courses = {
            'course_name': "NodeJS",
            'learn': ["ExpressJS", "MongoDb"],
            "platform": "youtube"
        }
        return Response(courses)

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def people(request):

    if request.method == 'GET':
        page = request.GET.get('page',1)
        page_size =1
        objs = Persons.objects.all()
        try:
            paginator = Paginator(objs, page_size)
            serializer = PeopleSerializer(paginator.page(page), many=True)
        except Exception as e:
            return Response({
                "status":False,
                "message":"No data"
            },status=status.HTTP_404_NOT_FOUND)


        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        obj = Persons.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj,data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PATCH':
        data = request.data
        obj = Persons.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        data = request.data
        obj = Persons.objects.get(id=data['id'])
        obj.delete()
        return Response({
            "Message":"Person Deleted"
        })

@api_view(["POST"])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)
    if serializer.is_valid():
        print(data)
        data = serializer.validated_data
        return Response({"message":"success"})
    return Response(serializer.errors)


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        objs = Persons.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data)
    def post(self,request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = Persons.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request):
        data = request.data
        obj = Persons.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self,request):
        data = request.data
        obj = Persons.objects.get(id=data['id'])
        obj.delete()
        return Response({
            "Message": "Person Deleted"
        })



class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Persons.objects.all()
    http_method_names = ['GET','POST','PUT']
    def list(self,request):
        search= request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
        serializer = PeopleSerializer(queryset,many=True)
        return Response({"status":200,"data":serializer.data},status=status.HTTP_206_PARTIAL_CONTENT)

    @action(detail = False,methods=['POST'])
    def send_mail_to_person(self,request):
        return Response({
            "status":True,
            "message":"action sample code"
        })



class RegisterAPI(APIView):
    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status":False,
                "data":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "status":True,
            "data":serializer.data
        },status=status.HTTP_201_CREATED)



class LoginAPI(APIView):
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response({"status":False,"message": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username = serializer.data['username'],password = serializer.data['password'])
        if not user:
            return Response({"status":400,"message":"Invalid credentials"},status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            "status":True,
            "message":"login successful",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },status=status.HTTP_200_OK)
