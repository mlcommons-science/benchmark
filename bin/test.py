
def _helper(x, y):
    """
    Helper method
    """
    return x**2 + y**2

def driver(x, y, z):
    """
    Main method
    """
    inter = _helper(x, y)
    return inter + z**2

driver(1, 2, 3)