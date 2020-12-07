import graphene
from graphene.types import interface
from graphene_django.types import DjangoObjectType
from .models import Employee, Department
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from graphql_relay import from_global_id
from graphql_jwt.decorators import login_required


class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee
        filter_fields = {
            "name": ["exact", "icontains"],
            "join_year": ["exact", "icontains"],
            "department__dept_name": ["icontains"],
        }
        interfaces = (relay.node,)


class DepartmentNode(DjangoObjectType):
    class Meta:
        model = Department
        filter_fields = {
            "employees": ["exact"],
            "dept_name": ["exact"],
        }
        interfaces = (relay.node,)


class Query(graphene.ObjectType):
    employee = graphene.Field(EmployeeNode, id=graphene.NonNull(graphene.ID))
    all_employees = DjangoFilterConnectionField(EmployeeNode)
    all_departments = DjangoFilterConnectionField(Department)

    @login_required
    def resolve_employee(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Employee.objects.get(id=from_global_id(id)[1])

    @login_required
    def resolve_all_employees(self, info, **kwargs):
        return Employee.objects.all()

    @login_required
    def resolve_all_departments(self, info, **kwargs):
        return Department.objects.all()
