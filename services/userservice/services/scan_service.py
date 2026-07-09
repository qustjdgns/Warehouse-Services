def validate_barcode(barcode):


    if barcode is None:

        return False, "바코드가 필요합니다."



    if len(str(barcode)) < 3:

        return False, "잘못된 바코드 형식입니다."



    return True, "정상 바코드"
