from django.urls import path
from employees import views
urlpatterns=[ 
    path('create',views.CreateEmployeeView.as_view(),name='create'),
    path('data',views.EmployeeDataView.as_view(),name='data'),
    path('employees',views.EmployeesListView.as_view(),name='employees'),
    path('employee-attend/<int:pk>',views.EmployeeAttendRecordsView.as_view(),name='employee-attend'),
    path('employee-attend/<int:employeeID>/<int:year>/<int:month>',views.EmployeeAttendInMonthView.as_view(),name='employee-attend-month'),
    path('employee-profile/<int:pk>',views.ProfileDataAdminView.as_view(),name='employee-profile'),
  ]