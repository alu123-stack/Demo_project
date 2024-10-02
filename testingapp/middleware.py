from django.http import JsonResponse

# class AuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         excluded_paths = ['/register/', '/login/','/admin/']
#         if request.path in excluded_paths:
#             return self.get_response(request)

#         if not request.user.is_authenticated:
#             return JsonResponse({"error": "Unauthorized"}, status=401)

#         response = self.get_response(request)
#         return response
    


