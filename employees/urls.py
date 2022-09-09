from django.urls import path
from employees import views
urlpatterns=[ 
    path('create',views.CreateEmployeeView.as_view(),name='create'),
    path('data',views.EmployeeDataView.as_view(),name='data'),
    path('employees',views.EmployeesListView.as_view(),name='employees'),
    path('employee-attend/<int:pk>',views.EmployeeAttendRecordsView.as_view(),name='employee-user'),
    path('employee-profile/<int:pk>',views.ProfileDataAdminView.as_view(),name='employee-profile'),
    path('add-mac',views.AddMacView.as_view(),name='add-mac'),
    path('addresses',views.MacAddressesListView.as_view(),name='addresses'),
]