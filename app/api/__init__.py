#
# The stoxs - ml (machine learning) application is implemented as a REST API (only). Cookie based access via a web browser is not supported.
# 
# The API is versioned using the URL path, e.g. /v1/stoxs/... and /v2/stoxs/... .
# 
# The endpoints are grouped by their functionality into subfolders as blueprints (Flask terminology) / APIs (Restx terminology).
# The api folder contains all services in subfolders.
# A subfolder is automatically registered as a blueprint / API if it contains a subfolder named endpoints.
#
# The API is secured using JWT tokens.
#
# Endpoints are documented using Swagger.
#
# Next to the endpoints there is a folder named models which contains the data models used by the namespaces of an API.
# 
