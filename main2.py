import xlwings as xw
import time

# --trusted-host pypi.org --trusted-host files.pythonhosted.or

def update_excel():

    wb = xw.Book(r"\\172.31.1.222\GlobalD\Derivatives\rawdata.xlsm")

    macro = wb.macro("Update_macro")

    macro()

    time.sleep(5)

    wb.save()
    wb.close()

    return


if __name__ == "__main__":
    update_excel()
