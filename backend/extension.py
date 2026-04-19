# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

# limiter = Limiter(
#     key_func=get_remote_address,
#     strategy="fixed-window",
#     # storage_uri="redis://localhost:6379",
#     default_limits=["200 per day", "100 per hour"]
# )