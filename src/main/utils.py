
def log_format(request, response, exception=None):
    user_id = request.user.id if request.user.is_authenticated else None
    user_info = {
        'user_id': user_id,
        'user_username': request.user.username if request.user.is_authenticated else ' ',
        'user_email': request.user.email if request.user.is_authenticated else ' ',
        'user_phone': request.user.phone if request.user.is_authenticated else ' ',
    }
    remote_host = request.META.get("REMOTE_ADDR",'-')
    request_line = f"{request.method} {request.get_full_path()} HTTP/1.1"
    status_code = response.status_code if not exception else 500
    response_size = response.get('Content-Length', ' ')
    referer = request.META.get('HTTP_REFERER', '-')
    elapsed_time = response.elapsed.total_seconds() if hasattr(response, 'elapsed') else None
    event = f"{request.resolver_match.app_names}.{request.resolver_match.url_name}"#{request.resolver_match.app_names}.{request.resolver_match.url_name}

    message = str(exception) if exception else 'Request is successfully'

    return {
        'user_info': user_info,
        'remote_host': remote_host,
        'request_line': request_line,
        'status_code': status_code,
        'response_size': response_size,
        'referer': referer,
        'elapsed_time': elapsed_time,
        'message': message,
        'event': event
    }
