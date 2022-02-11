import xlsxwriter
import os


async def create_exel(users):
    file_name = 'users.xlsx'
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    for row, user in enumerate(users):
        for col, data in enumerate(user):
            worksheet.write(row, col, str(data))

    workbook.close()
    return file_name


async def delete_file(file_path):
    os.remove(file_path)
