def is_raw(codec):
    """ resolve genorators that produce raw bytes """
    if codec is 'jpeg' or codec is 'pdf':
        return True
    
    return False