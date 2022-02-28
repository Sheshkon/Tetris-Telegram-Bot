import xlsxwriter
import os


def write_worksheet(worksheet, table_name):
    for row, user in enumerate(table_name):
        for col, data in enumerate(user):
            worksheet.write(row, col, str(data))


def create_exel(users, chats):
    file_name = 'bot_bd.xlsx'
    workbook = xlsxwriter.Workbook(file_name)

    worksheet = workbook.add_worksheet()
    write_worksheet(worksheet, users)

    worksheet = workbook.add_worksheet()
    write_worksheet(worksheet, chats)

    workbook.close()
    return file_name


def delete_file(file_path):
    os.remove(file_path)
