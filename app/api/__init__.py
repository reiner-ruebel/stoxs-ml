#
# The stoxs - ml (machine learning) application is implemented as a REST API (only). Cookie based access via a web browser is not supported.
# 
# The API is versioned using the URL path, e.g. /v1/stoxs/... and /v2/stoxs/... .
# 
# The endpoints are grouped by their functionality into subfolders as blueprints (Flask terminology) / namespaces (Restx terminology).
# The api folder contains all services in subfolders.
# A subfolder is automatically registered as a blueprint / namespace if it contains a subfolder named endpoints.
#
# The API is secured using JWT tokens.
#
# Endpoints are documented using Swagger.
# 
