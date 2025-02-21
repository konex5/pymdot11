def automation():
    return True

def is_fmdot_available():
    try:
        import fmd_operators
    except:
        return False
    return True
