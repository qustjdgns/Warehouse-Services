def validate_barcode(barcode):
    # barcode 값이 없는 경우
    if not barcode:
        return False, "barcode 값이 필요합니다."

    # barcode 값이 문자열이 아닌 경우
    if not isinstance(barcode, str):
        return False, "barcode 값은 문자열이어야 합니다."

    # barcode 길이가 너무 짧은 경우
    if len(barcode) < 2:
        return False, "barcode 값이 너무 짧습니다."

    return True, "valid"
