def automation():
    return True


def is_mdot_available():
    try:
        import mdot_operators
    except:
        return False
    return True
