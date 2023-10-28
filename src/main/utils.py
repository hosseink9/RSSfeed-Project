
def log_format(request, response, exception=None):
    user_id = request.user.id if request.user.is_authenticated else None
    user_info = {
        'user_id': user_id,
        'user_username': request.user.username if request.user.is_authenticated else ' ',
        'user_email': request.user.email if request.user.is_authenticated else ' ',
        'user_phone': request.user.phone if request.user.is_authenticated else ' ',
    }
    remote_host = request.META.get("REMOTE_ADDR",'-')
    request_line = request.method

    status_code = response.status_code if not exception else 500
    response_size = response.get('Content-Length', ' ') if response else ' '
    referrer = request.META.get('HTTP_REFERRER', '-')
    elapsed_time = response.elapsed.total_seconds() if hasattr(response, 'elapsed') else None
    user_agent=request.headers.get("user-agent")
    event = f"{request.get_full_path()} HTTP/1.1"

    # event = f"{request.resolver_match.app_names[0]}.{request.resolver_match.url_name}" if request.resolver_match.app_names else ' '
    # event = f"api.{request.resolver_match.app_name}.{request.resolver_match.url_name}"
    # event = request.resolver_match.url_name

    message = str(exception) if exception else 'Request is successfully'

    return {
        'user_info': user_info,
        'remote_host': remote_host,
        'request_line': request_line,
        'status_code': status_code,
        'response_size': response_size,
        'referrer': referrer,
        'elapsed_time': elapsed_time,
        'message': message,
        'user_agent': user_agent,
        'event': event,
    }



def authentication_log_format(user,body, exception=None):

    message = str(exception) if exception else 'Consume is successfully'


    return {
        'user_id': str(user.id ),
        'user_phone': str(user.phone),
        'user_agent': body["user_agent"],
        'event': f"consumer.{body['routing_key']}",
        "status": "success",
        'message': message
    }

