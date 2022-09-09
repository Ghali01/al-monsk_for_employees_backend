from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CreateEmployeeSerializer, MACAddressSerilizer,ReadEmployeeSerializer,AttendRecordSerializer
from .models import AttendRecord,Employee,MACAdders
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class CreateEmployeeView(APIView):
    

    def post(self,request):
        ser1=CreateEmployeeSerializer(data=request.data)
        if ser1.is_valid(raise_exception=True):
            ser1.save()
            ser2=ReadEmployeeSerializer(instance=ser1.instance)
            return Response(ser2.data,201)
class EmployeesListView(ListAPIView):
    serializer_class=ReadEmployeeSerializer
    queryset=Employee.objects.all()


class EmployeeDataView(APIView):

    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request):
        ser=ReadEmployeeSerializer(instance=request.user.employee)
        return Response(ser.data)

class EmployeeAttendRecordsView(ListAPIView):
    serializer_class=AttendRecordSerializer
    queryset=AttendRecord.objects.all()

    dateParm=openapi.Parameter('date',in_=openapi.IN_QUERY,type=openapi.TYPE_STRING)

    def filter_queryset(self, queryset):

        queryset=queryset.filter(employee_id=self.kwargs['pk'])
        if 'date' in self.request.GET:
            queryset=queryset.filter(time__date=self.request.GET['date']) 
        return queryset
    @swagger_auto_schema(manual_parameters=[dateParm])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class AddMacView(CreateAPIView):
    serializer_class=MACAddressSerilizer



class MacAddressesListView(ListAPIView):
    queryset=MACAdders.objects.all()
    serializer_class=MACAddressSerilizer

class ProfileDataAdminView(RetrieveAPIView):
    queryset=Employee.objects.all()
    serializer_class=ReadEmployeeSerializer
    