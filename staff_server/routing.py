from django.urls import path
from employees import consumers

url_patterns=[ 
    path('ws/attend',consumers.AttendConsumer.as_asgi())
]