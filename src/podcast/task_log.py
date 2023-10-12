import logging
import json

logger = logging.getLogger('elastic-logger')


def log_task_info(task_name, level, message, task_id, args, kwargs, retval=' ', exception=' ', retry_count=' ',max_retries=' ', retry_eta=' '):

    log_data = {
        'level': level,
        'message': message,
        'task_id': task_id,
        'task_name': task_name,
        'args': args,
        'kwargs': kwargs,
        'input_data': {
            'args': args,
            'kwargs': kwargs
        },
        'output_data': retval,
        'exception': str(exception) if exception else None,
        'retry_count': retry_count,
        'max_retries': max_retries,
        'retry_eta': retry_eta
    }
    logger.log(getattr(logging, level.upper()), json.dumps(log_data))