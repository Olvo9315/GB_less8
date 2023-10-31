import os

def read_txt(filename):
    phone_book=[]
    fields = ['Фамилия', 'Имя', 'Телефон', 'Описание']
    
    with open(filename, 'r', encoding='utf-8') as phb:
        for line in phb:
            record = dict(zip(fields, line.strip().split(',')))
            phone_book.append(record)
            
    return phone_book

def write_txt(filename, pb):
    with open(filename, 'w', encoding='utf-8') as pb_out:
        for i in range(len(pb)):
            s = ''
            for v in pb[i].values():
                s += v + ','
            pb_out.write(f'{s[:-1]}\n')
            
def show_menu():
    print('\nМеню')
    print('1. Распечатать справочник',
          '2. Найти телефон по фамилии',
          '3. Изменить номер телефона',
          '4. Удалить запись',
          '5. Найти абонента по номеру телефона',
          '6. Добавить абонента в справочник',
          '7. Копировать данные с другого файла',
          '8. Закончить работу', sep='\n'
          )
    while True:
        try:
            choice = int(input('\nВыберите опцию: '))
            if 1 <= choice <= 8:
                return choice
            else:
                print("Пожалуйста, выберите число от 1 до 8.")
        except ValueError:
            print("Пожалуйста, введите целое число.")
          
def print_result(pb):
    if pb:
        fields = ['Фамилия', 'Имя', 'Телефон', 'Описание']
        max_lengths = {field: max(len(str(record[field])) for record in pb) for field in fields}

        print(" | ".join(f"{field:<{max_lengths[field]}}" for field in fields))
        print("-" * (sum(max_lengths.values()) + len(fields) * 3 - 1))

        for index, record in enumerate(pb, start=1):
            print(f"{index}. " + " | ".join(f"{str(record[field]):<{max_lengths[field]}}" for field in fields))
    else:
        print("Справочник пуст.")
        
def find_by_lastname(pb, last_name):
    records = [record for record in pb if record['Фамилия'] == last_name]
    return records if records else f"Абонент с фамилией '{last_name}' не найден."

def change_number(pb, last_name, new_number):
    for record in pb:
        if record['Фамилия'] == last_name:
            record['Телефон'] = new_number
            write_txt('phonebook.txt', pb)
            return f"Номер телефона для '{last_name}' изменен на '{new_number}'."
    return f"Абонент с фамилией '{last_name}' не найден."

def delete_by_lastname(pb, last_name):
    records = [record for record in pb if record['Фамилия'] == last_name]
    if records:
        pb.remove(records[0])
        write_txt('phonebook.txt', pb)
        return f"Абонент с фамилией '{last_name}' удален."
    else:
        return f"Абонент с фамилией '{last_name}' не найден."
    
def find_by_number(pb, number):
    records = [record for record in pb if record['Телефон'] == number]
    return records if records else f"Абонент с номером '{number}' не найден."

def add_user(pb, last_name, user_name, tel_number, comment):
    new_record = {'Фамилия': last_name, 'Имя': user_name, 'Телефон': tel_number, 'Описание': comment}
    pb.append(new_record)
    write_txt('phonebook.txt', pb)
    return f"Абонент '{last_name}' успешно добавлен в справочник."

def select_file_from_list(text):
    current_directory = os.getcwd()
    txt_files = [file for file in os.listdir(current_directory) if file.endswith(".txt")]
    if not txt_files:
        print("В текущей директории нет .txt файлов. Создайте справочник")
        return None
    print(f"\n{text}")
    for index, txt_file in enumerate(txt_files, start=1):
        print(f"{index}. {txt_file}")
    while True:
        try:
            choice = int(input("Выберите номер файла (или 0 для отмены): "))
            if 0 <= choice <= len(txt_files):
                return txt_files[choice - 1] if choice > 0 else 0
            else:
                print("Неверный выбор. Пожалуйста, выберите номер файла из списка.")
        except ValueError:
            print("Пожалуйста, введите целое число.")

def select_line_from_pb(pb_from):
    print_result(pb_from)
    while True:
        try:
            choice = int(input("Выберите номер строки для копирования (или 0 для отмены): "))
            if 0 <= choice <= len(pb_from):
                return pb_from[choice - 1] if choice > 0 else None
            else:
                print("Неверный выбор. Пожалуйста, выберите номер строки из списка.")
        except ValueError:
            print("Пожалуйста, введите целое число.")

def select_data_from_line(line):
    return line['Фамилия'], line['Имя'], line['Телефон'], line['Описание']


def main():
    choice = show_menu()
    # print(choice)
    pb = read_txt('phonebook.txt')
    while (choice != 8):
        if choice == 1:
            print_result(pb)
        elif choice == 2:
            last_name = input('Фамилия: ')
            print(find_by_lastname(pb, last_name))
        elif choice == 3:
            last_name = input('Фамилия: ')
            new_number = input('Новый номер: ')
            print(change_number(pb, last_name, new_number))
        elif choice == 4:
            last_name = input('Фамилия: ')
            print(delete_by_lastname(pb, last_name))
        elif choice == 5:
            number = input('Номер: ')
            print(find_by_number(pb, number))
        elif choice == 6:
            last_name = input('Фамилия: ')
            user_name = input('Имя: ')
            tel_number = input('Телефон: ')
            comment = input('Описание: ')
            add_user(pb, last_name, user_name, tel_number, comment)
        elif choice == 7:
            selected_file = select_file_from_list('Копировать из файла: ')
            if selected_file == 0:
                print('\nВыбор отменён')
            else: 
                pb_from = read_txt(selected_file)
                line = select_line_from_pb(pb_from)
                last_name, user_name, tel_number, comment = select_data_from_line(line)
                add_user(pb, last_name, user_name, tel_number, comment)
            
        choice = show_menu()
    
if __name__ == '__main__':
    main()