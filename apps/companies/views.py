from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.cache import cache_response, RedisCacheMixin

from .models import Company
from .serializers import CompanySerializer
from .services import CompanyService


@api_view(["GET"])
@cache_response('company')
def get_companies(request):

    companies = CompanyService.get_all_companies()

    serializer = CompanySerializer(companies, many=True, context={'request': request})

    return Response(serializer.data)


@api_view(["POST"])
@cache_response('company')
def create_company(request):

    serializer = CompanySerializer(data=request.data, context={'request': request})

    if serializer.is_valid():

        company = CompanyService.create_company(serializer.validated_data)

        return Response(CompanySerializer(company, context={'request': request}).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors)


@api_view(["PUT"])
@cache_response('company')
def update_company(request, company_id):

    company = Company.objects.get(id=company_id)

    serializer = CompanySerializer(company, data=request.data, context={'request': request})

    if serializer.is_valid():

        company = CompanyService.update_company(company, serializer.validated_data)

        return Response(CompanySerializer(company, context={'request': request}).data)

    return Response(serializer.errors)


@api_view(["DELETE"])
@cache_response('company')
def delete_company(request, company_id):

    company = Company.objects.get(id=company_id)

    CompanyService.delete_company(company)

    return Response({"message": "Company deleted"})

from rest_framework import viewsets

class CompanyViewSet(RedisCacheMixin, viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer