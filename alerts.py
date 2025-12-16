def check_zscore_alert(z, threshold):
    if z is None:
        return False
    return abs(z) > threshold
