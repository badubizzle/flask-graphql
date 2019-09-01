from timeit import default_timer as timer

def timing_middleware(logger):

    def inner_timing_middleware(next, root, info, **args):    
        start = timer()
        return_value = next(root, info, **args)
        duration = timer() - start
        logger.debug("{parent_type}.{field_name}: {duration} ms".format(
            parent_type=root._meta.name if root and hasattr(root, '_meta') else '',
            field_name=info.field_name,
            duration=round(duration * 1000, 2)
        ))
        return return_value
    return inner_timing_middleware
