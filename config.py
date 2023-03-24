###### Postgres Driver example
# ==============================
# DATABASE_DRIVERS = {
#     "driver": "database.mongo",
#     "config": {
#         "connection_uri": "mongodb cluster connection uri",
#         "database_name": "database name",
#         "collection_name": "collection name"
#     }
# }

DATABASE_DRIVERS = {
    "driver": "database.postgres",
    "config": {
        "connection_uri": "postgresql://localhost/alex_testing?user=alex&password=euu",
        "max_size": 100,  # the maximum amount of connections to create for the PostgreSQL connection pool
        "min_size": 75,  # the minimum amount of connections to create for the PostgreSQL connection pool
        "table_name": "major_project",  # the name of the table to use for the database
    },
}

CACHE_DRIVERS = {
    "driver": "cache.memorycache",  # basic in memory cache. Cleared everytime your node shutsdown.
    "config": {}  # leave this empty as memory caches have no config
    # apart from the MAX_CACHE_SIZE which is inferred from the setting automatically.
}

##### Redis Cache Driver example
# ==============================
# CACHE_DRIVERS = {
#     "driver": "cache.rediscache",
#     "config": {
#         "connection_uri": "redis connection uri",
#         "username": "username for auth",
#         "password": "password for auth"
#         # please REMOVE the username and password keys if your redis instance
#         # does not require username and password authentication
#         # OR if your connection uri includes these details.
#     }
# }

MAX_CACHE_SIZE = 100  # set a maximum cache size. If you want a cache with no limit -
# simply set this value to 'inf'. This setting is useful if you have a limited amount
# of memory to work with. THIS APPLIES ONLY TO THE IN MEMORY DATABASE.

ALLOWED_HOSTS = ["*"]  # set a list of allowed hosts.
# by default, this is set to ALL hosts, as indicated through the '*'
# this internally uses Starlette's Trusted Host middleware (starlette.middleware.trustedhost.TrustedHostMiddleware)

ENFORCE_SECURE_SCHEME = False  # any incoming requests must be from,
# the https or wss protocols. Any other protcol will be redirected to their secure variant.

CORS_ALLOWED_ORIGINS = ["*"]  # a list of allowed origins
# that browsers are allowed to use in a Cross-Domain context.
# by default, this is set to all domains.

SECRET_KEY = "SET_A_CUSTOM_KEY"  # a secret key that will be checked in the 'Authorization' header
# whenever a POST request is made to /delete endpoint.

ALLOWED_HOSTS = ["*"]  # set a list of allowed hosts.
# by default, this is set to ALL hosts, as indicated through the '*'
# this internally uses Starlette's Trusted Host middleware (starlette.middleware.trustedhost.TrustedHostMiddleware)

REQUIRE_AUTH_FOR_DELETE = True  # whether authorization is needed via the secret key
# to delete the file

LOG_FILE = "logs.log"  # the name of the log file to use for logging requests.
# this is set to 'logs.log' by default.
