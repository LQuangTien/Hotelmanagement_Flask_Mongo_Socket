from datetime import datetime
from flask import url_for, request
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from werkzeug.utils import redirect
from mainapp import admin
from flask_admin.contrib.mongoengine import ModelView
from mainapp.models_mongodb import users, rooms, reservations, regulation, messages
from mainapp.services import report
from mainapp.services.report import MyBarGraph


class AuthenticatedView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.role == 1

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('login_admin', next=request.url))


class CustomAuthenticatedView(BaseView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.role == 1

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('login_admin', next=request.url))


class aboutUsView(CustomAuthenticatedView):
  @expose('/')
  def index(self):
    return self.render('admin/aboutus.html')


class ReportView(CustomAuthenticatedView):
  @expose('/')
  def index(self):
    args = request.args if request.args else None

    salesMonth = int(args.get('salesMonth')) if args else datetime.now().month
    salesYear = int(args.get('salesYear')) if args else datetime.now().year

    usedMonth = int(args.get('usedMonth')) if args else datetime.now().month
    usedYear = int(args.get('usedYear')) if args else datetime.now().year

    data, types = report.getReservationByQuery("total", salesMonth, salesYear)
    salesChart = MyBarGraph(data, types, "Biểu đồ tỉ lệ doanh thu theo từng loại phòng")
    salesChartJSON = salesChart.get()
    data2, types2 = report.getReservationByQuery("dayTotal", usedMonth, usedYear)
    usedChart = MyBarGraph(data2, types, "Biểu đồ tỉ lệ sử dụng theo từng loại phòng")
    usedChartJSON = usedChart.get()

    return self.render('admin/chart.html',
                       salesChartJSON=salesChartJSON, usedChartJSON=usedChartJSON,
                       salesMonth=salesMonth, salesYear=salesYear,
                       usedMonth=usedMonth, usedYear=usedYear)


class logoutView(BaseView):
  @expose('/')
  def index(self):
    logout_user()
    return self.render('admin/index.html')

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('login_admin', next=request.url))


class UserView(AuthenticatedView):
  column_exclude_list = ['password', ]


admin.add_view(ReportView(name='Monthly Report'))
admin.add_view(UserView(users))
admin.add_view(AuthenticatedView(rooms))
admin.add_view(AuthenticatedView(reservations))
admin.add_view(AuthenticatedView(regulation))
admin.add_view(AuthenticatedView(messages))
admin.add_view(aboutUsView(name='About us'))
admin.add_view(logoutView(name='Logout'))
