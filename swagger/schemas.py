from drf_yasg.inspectors import SwaggerAutoSchema


class CustomActionNoParametersSchema(SwaggerAutoSchema):

    def get_query_parameters(self):
        return []

    def get_request_body_parameters(self, consumes):
        return []
