from tkinter import *
from tkinter import messagebox as mb
import pymorphy3

# Функция для начала игры
def Start_Game():
    global root, bot, click_count, statistics_click_start
    click_count = 0
    bot = cities.pop()  # Получаем первый город из множества
    state = TextPole.cget("state")
    TextPole.configure(state=NORMAL)
    initial_text = ("Привет, Игрок! Суть игры назвать как можно больше городов."
                    "\nВ твоем арсенале имеются 3 подсказки. Чтобы отправить город напишите его, затем нажмите Enter."
                    " Учти, что писать город   нужно с заглавной буквы. Удачной игры!\n")
    current_text = TextPole.get("1.0", END).strip()
    if state == "normal":
        if current_text:  # Проверка на пустоту текста
            response = mb.askyesno("Предупреждение", "Вы уверены, что хотите начать заново?")
            if response:
                statistics_click_start += 1
                TextPole.delete("1.0", END)  # Удаление всего текста
                TextPole.insert(END, initial_text)  # Добавление начального текста
                TextPole.insert(END, "\n>>>>>>>> БОТ: " + bot)
                if bot[-1] not in sim:
                    TextPole.insert(END, '\nВам на букву "' + bot[-1] + '".\n')
                elif bot[-1] in sim:
                    TextPole.insert(END, '\nВам на букву "' + bot[-2] + '".\n')
        else:
            statistics_click_start += 1
            TextPole.insert(END, initial_text)  # Добавление начального текста
            TextPole.insert(END, "\n>>>>>>>> БОТ: " + bot)
            if bot[-1] not in sim:
                TextPole.insert(END, '\nВам на букву "' + bot[-1] + '".\n')
            elif bot[-1] in sim:
                TextPole.insert(END, '\nВам на букву "' + bot[-2] + '".\n')
    else:
        TextPole.delete("1.0", END)  # Удаление всего текста
        statistics_click_start += 1
        TextPole.insert(END, initial_text)  # Добавление начального текста
        bot = cities.pop()
        TextPole.insert(END, "\n>>>>>>>> БОТ: " + bot)
        if bot[-1] not in sim:
            TextPole.insert(END, '\nВам на букву "' + bot[-1] + '".\n')
        elif bot[-1] in sim:
            TextPole.insert(END, '\nВам на букву "' + bot[-2] + '".\n')
    TextPole.tag_add("highlight", "1.0", "3.0")
    TextPole.tag_config("highlight", background="yellow")

# Функция для получения правильного склонения слова "город"
def deviation(n):
    word = 'город'
    parsed_word = morph.parse(word)[0]
    return parsed_word.make_agree_with_number(n).word

# Функция для завершения игры
def Over_Game():
    global record, original_record, delete_cities
    TextPole.insert(END, f"\nИгра окончена! Вы назвали {str(record)} {deviation(record)}")
    TextPole.configure(state=DISABLED)
    if record > original_record:
        if original_record != 0:
            mb.showinfo("Информация",f"Поздравляю, Игрок! Вы побили свой рекорд!"
                                     f"\nВы назвали {record} {deviation(record)}")
        original_record = record
        record_label.config(text=f'Ваш рекорд\n{original_record} {deviation(record)}')
    record = 0
    cities.update(delete_cities)  # Восстанавливаем множество городов
    delete_cities.clear()

# Функция, которая запускается при нажатии клавиши пользователем
def Game_Started(event):
    global bot, sim, record, delete_cities, statistics_click_user,original_record
    user = ""
    text = event.widget.get("1.0", "end-1c")  # Получаем весь текст из виджета
    TextPole_lines = text.split('\n')
    user_lines = len(TextPole_lines)
    if user_lines % 5 >= 0 and user_lines % 5 <= 4:  # Проверка текста юзера
        user += TextPole_lines[user_lines - 1]  # Запоминаем город юзера
    if event.keysym == "Return" and user:
        # Списки доступных городов
        existing_cities_1 = {city for city in cities if city.lower()[0] == user[-1]}
        existing_cities_2 = {city for city in cities if city.lower()[0] == user[-2]}
        if user in delete_cities:
            mb.showerror("Ошибка",'Такой город уже называли.')
        elif user not in cities:
            mb.showerror("Ошибка", 'Такого города не существует! Попробуйте снова.')
        else:
            if bot[-1] not in sim:
                if user.lower()[0] != bot[-1]:
                    mb.showerror("Ошибка", f"Неправильно. город должен начинаться с буквы '{bot[-1]}'")
                elif user.lower()[0] == bot[-1]:
                    record += 1
                    statistics_click_user += 1
                    TextPole.insert(END, '\nВерно!')
                    if user[-1] not in sim:
                        TextPole.insert(END, f"\nМне на букву '{user[-1]}'.")
                    elif user[-1] in sim and existing_cities_1:
                        TextPole.insert(END, f"\nМне на букву '{user[-2]}'.")
                    elif user[-1] in sim and not existing_cities_1:
                        TextPole.insert(END, f"\nМне на букву '{user[-2]}'.")
                    delete_cities.add(user)
                    cities.remove(user)
                    if existing_cities_1:  # Проверяем, есть ли еще города на последнюю букву
                        for candidate in existing_cities_1:
                            if candidate.lower()[0] == user[-1]:
                                bot = candidate
                                delete_cities.add(candidate)
                                cities.remove(candidate)
                                TextPole.insert(END, '\n>>>>>>>> БОТ: ' + candidate)
                                if candidate[-1] in sim:
                                    TextPole.insert(END, '\nВам на букву "' + candidate[-2] + '".')
                                else:
                                    TextPole.insert(END, '\nВам на букву "' + candidate[-1] + '".')
                                break
                    elif not existing_cities_1 and existing_cities_2:
                        for candidate in existing_cities_2:
                            if candidate.lower()[0] == user[-2]:
                                bot = candidate
                                delete_cities.add(candidate)
                                cities.remove(candidate)
                                TextPole.insert(END, '\n>>>>>>>> БОТ: ' + candidate)
                                if candidate[-1] in sim:
                                    TextPole.insert(END, '\nВам на букву "' + candidate[-2] + '".')
                                else:
                                    TextPole.insert(END, '\nВам на букву "' + candidate[-1] + '".')
                                break
                    elif not existing_cities_1 and not existing_cities_2:
                        mb.showinfo("Информация", f"Игра окончена. Города закончились.")
                        TextPole.insert(END, f"\nИгра окончена! Вы назвали {str(record)} {deviation(record)}")
                        TextPole.configure(state=DISABLED)
                        if record > original_record:
                            if original_record != 0:
                                mb.showinfo("Информация", f"Поздравляю, Игрок! Вы побили свой рекорд!"
                                                          f"\nВы назвали {record} {deviation(record)}")
                            original_record = record
                            record_label.config(text=f'Ваш рекорд\n{original_record} {deviation(record)}')
                        record = 0
                        cities.update(delete_cities)  # Восстанавливаем множество городов
                        delete_cities.clear()
            elif bot[-1] in sim or not existing_cities_1:
                if user.lower()[0] != bot[-2]:
                    mb.showerror("Ошибка", f"Неправильно. город должен начинаться с буквы '{bot[-2]}'.")
                else:
                    record += 1
                    statistics_click_user += 1
                    TextPole.insert(END, '\nВерно!')
                    if user[-1] not in sim:
                        TextPole.insert(END, f"\nМне на букву '{user[-1]}'.")
                    elif user[-1] in sim and existing_cities_1:
                        TextPole.insert(END, f"\nМне на букву '{user[-2]}'.")
                    elif user[-1] in sim and not existing_cities_1:
                        TextPole.insert(END, f"\nМне на букву '{user[-2]}'.")
                    delete_cities.add(user)
                    cities.remove(user)
                    if existing_cities_1:  # Проверяем, есть ли еще города на последнюю букву
                        for candidate in existing_cities_1:
                            if candidate.lower()[0] == user[-1]:
                                bot = candidate
                                delete_cities.add(candidate)
                                cities.remove(candidate)
                                TextPole.insert(END, '\n>>>>>>>> БОТ: ' + candidate)
                                if candidate[-1] in sim:
                                    TextPole.insert(END, '\nВам на букву "' + candidate[-2] + '".')
                                else:
                                    TextPole.insert(END, '\nВам на букву "' + candidate[-1] + '".')
                                break
                            elif not existing_cities_1:
                                for candidate in existing_cities_2:
                                    if candidate.lower()[0] == user[-2]:
                                        bot = candidate
                                        delete_cities.add(candidate)
                                        cities.remove(candidate)
                                        TextPole.insert(END, '\n>>>>>>>> БОТ: ' + candidate)
                                        if candidate[-1] in sim:
                                            TextPole.insert(END, '\nВам на букву "' + candidate[-2] + '".')
                                        else:
                                            TextPole.insert(END, '\nВам на букву "' + candidate[-1] + '".')
                                        break
                            elif not existing_cities_1 and not existing_cities_2:
                                mb.showinfo("Информация", f"Игра окончена. Города закончились.")
                                TextPole.insert(END, f"\nИгра окончена! Вы назвали {str(record)} {deviation(record)}")
                                TextPole.configure(state=DISABLED)
                                if record > original_record:
                                    if original_record != 0:
                                        mb.showinfo("Информация", f"Поздравляю, Игрок! Вы побили свой рекорд!"
                                                                  f"\nВы назвали {record} {deviation(record)}")
                                    original_record = record
                                    record_label.config(text=f'Ваш рекорд\n{original_record} {deviation(record)}')
                                record = 0
                                cities.update(delete_cities)  # Восстанавливаем множество городов
                                delete_cities.clear()

# Функция для кнопки подсказки
def Clue_Button():
    global bot, click_count, statistics_click_clue
    state = TextPole.cget("state")
    statistics_click_clue += 1
    click_count += 1
    if click_count <= 3 and state == "normal":
        for city in cities:
            if bot[-1] not in sim:
                if city[0].lower() == bot[-1].lower():
                    mb.showinfo("Город", f"Попробуйте город - {city}")
                    return
            elif bot[-1] in sim:
                if city[0].lower() == bot[-2].lower():
                    mb.showinfo("Город", f"Попробуйте город - {city}")
                    return
        mb.showinfo("Город", "Не найдено подходящего города.")
    elif state == "disabled":
        mb.showerror(title="Ошибка", message="Игра не запущена.")
    elif click_count > 3:
        mb.showerror(title="Ошибка", message='Вы потратили все подсказки')

# Функция для вывода статистики
def Statistics_button():
    global statistics_click_start, statistics_click_clue, statistics_click_user, user_cities
    mb.showinfo("Статистика о сессии",
                f"Запущенно игр - {statistics_click_start}\n"
                f"Названо городов - {statistics_click_user}\n"
                f"Использовано подсказок - {statistics_click_clue}\n")
# Создание главного окна
root = Tk()
root.resizable(False, False)
root.title("Игра в города")
c = Canvas(root, width=740, height=720)
c.pack(anchor=CENTER, expand=1)

# Загрузка городов из файла и их перемешивание
with open("Cities", encoding="utf-8") as file:
    lines = file.readlines()
cities_list = []
for idx, line in enumerate(lines):
    words = line.split()
    for word in words:
        cities_list.append((word))
cities = set(cities_list)
delete_cities = set()
user_cities = []

morph = pymorphy3.MorphAnalyzer() # вызов конструктора класса MorphAnalyzer.
sim = ('ъ', 'ь', 'ы', 'ё', 'й')  # Кортеж символов исключений.
bot = cities.pop()
click_count = 0
original_record = 0
record = 0
statistics_click_start = 0
statistics_click_user = 0
statistics_click_clue = 0
gor = ""
candidate = ""

# Создание текстового поля и кнопок
TextPole = Text(root, width=60, height=28, bg="white")
TextPole.place(relx=0.08, rely=0.02)
TextPole.config(state=DISABLED)

Start = Button(root, text="Начать игру", width="25", height="4", command=Start_Game)
game_off = Button(root, text="Закончить", width="25", height="4", command=Over_Game)
clue_button = Button(root, text='Подсказка', width="16", height="4", command=Clue_Button)
statistics_button = Button(root, text='Статистика', width="16", height="4", command=Statistics_button)
record_label = Label(root, text="Ваш рекорд\n0 городов", font='Times 20')

record_label.place(relx=0.75, rely=0.08)
Start.place(relx=0.08, rely=0.7)
game_off.place(relx=0.4, rely=0.7)
clue_button.place(relx=0.75, rely=0.25)
statistics_button.place(relx=0.75, rely=0.40)
TextPole.bind("<KeyPress>", Game_Started)

root.mainloop()
