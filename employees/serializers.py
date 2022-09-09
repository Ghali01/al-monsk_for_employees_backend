from rest_framework.serializers import ModelSerializer,CharField,TimeField,IntegerField,Serializer,BooleanField
from django.contrib.auth import get_user_model
from .models import AttendRecord, Employee,MACAdders


class AttendRecordSerializer(ModelSerializer):

    class Meta:
        model=AttendRecord
        fields='__all__'


class CreateEmployeeSerializer(Serializer):
    email=CharField()
    firstName=CharField()
    secondName=CharField()
    start=TimeField()
    end=TimeField()
    # class Meta:
    #     model=get_user_model()
    #     fields=['email','firstName','secondName','start','end']

    def create(self, validated_data):
        user=get_user_model().objects.create(firstName=validated_data['firstName'],secondName=validated_data['secondName'],email=validated_data['email'])
        
        employee=Employee.objects.create(start=validated_data['start'],end=validated_data['end'],user=user)
        return employee
class ReadEmployeeSerializer(ModelSerializer):
    email=CharField(source='user.email')
    online=BooleanField(source='user.online')
    firstName=CharField(source='user.firstName')
    secondName=CharField(source='user.secondName')
    token=CharField(read_only=True,source='user.token.key')
    userID=IntegerField(source='user.id')
    class Meta:
        model=Employee
        fields=['email','firstName','secondName','start','end','online','token','id','userID']



class MACAddressSerilizer(ModelSerializer):

    class Meta:
        model=MACAdders
        fields='__all__'