from take_FTP import get_last_file_from_ftp
from bitrix_create_product import create_products_from_csv


def main():
    get_last_file_from_ftp()
    create_products_from_csv()


if __name__ == '__main__':
    main()
