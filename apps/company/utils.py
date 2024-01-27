from drf_yasg import openapi


def company_id_header_params():
    company = openapi.Parameter(
        'company',
        openapi.IN_HEADER,
        description="company",
        type=openapi.IN_HEADER
    )
    return [company]
