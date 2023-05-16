import utils
import os.path


json_path = os.path.join('operation.json')

def main():
    ''' Открываем файл, запускаем сортировку, выводим результат'''
    new_peremennaia = utils.read_file(json_path)
    exe_sorted_by_date = utils.format_dates(new_peremennaia)
    utils.show_transactions(exe_sorted_by_date)


if __name__ == '__main__':
    main()

