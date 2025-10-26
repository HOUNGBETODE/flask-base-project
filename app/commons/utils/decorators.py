from functools import wraps

def swagger_doc(docstring):
    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)
        
        wrapped_func.__doc__ = docstring
        return wrapped_func
    
    return decorator
