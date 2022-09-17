from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CreateEmployeeSerializer,ReadEmployeeSerializer,AttendRecordSerializer
from .models import AttendRecord,Employee
from django.utils import timezone
from calendar import monthrange
from django.shortcuts import get_object_or_404
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


    def filter_queryset(self, queryset):

        queryset=queryset.filter(employee_id=self.kwargs['pk'])
        if 'date' in self.request.GET:
            queryset=queryset.filter(time__date=self.request.GET['date']) 
        return queryset
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProfileDataAdminView(RetrieveAPIView):
    queryset=Employee.objects.all()
    serializer_class=ReadEmployeeSerializer
    

class EmployeeAttendInMonthView(APIView):


    def get(self,request,employeeID,year,month):
        employee=get_object_or_404(Employee,id=employeeID)
        startAsDate=timezone.datetime.combine(timezone.datetime.now().date(),employee.start)
        endAsDate=timezone.datetime.combine(timezone.datetime.now().date(),employee.end)
        delta=timezone.timedelta(minutes=30)
        startBefore=(startAsDate-delta).time()
        startAfter=(startAsDate+delta).time()
        endBefore=(endAsDate-delta).time()
        endAfter=(endAsDate+delta).time()
        days=monthrange(year,month)[1]
        attends=[] 
        for day in range(1,days+1):
            date=timezone.datetime(year,month,day).date()
            start=AttendRecord.objects.filter(time__date=date,time__time__gte=startBefore,time__time__lte=startAfter).exists()
            end=AttendRecord.objects.filter(time__date=date,time__time__gte=endBefore,time__time__lte=endAfter).exists()
            attends.append({
                'data':date.strftime('%Y-%m-%d'),
                'start':start,
                'end':end,
            })
        return Response(attends)