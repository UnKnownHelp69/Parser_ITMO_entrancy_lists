import requests
import sys
from bs4 import BeautifulSoup


indexes = [2298]

for ind in range(2190, 2216):
    indexes.append(ind)

for ind in indexes:
    uni = "ITMO"
    dir = "01.03.02"
    url = 'https://abit.itmo.ru/rating/bachelor/budget/' + str(ind)

    arr_celevoe_kvota = []
    arr_osobaya_kvota = []
    arr_otdelnaya_kvota = []
    arr_bvi_kvota = []
    arr_all_kvota = []

    all_users_inf = []

    def parse_numbers(url, selector):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.select(selector)
            return elements
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
        except Exception as e:
            print(f"Ошибка при парсинге: {e}")
            return None

    def parse_all(url, selector):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.select(selector)
            return elements
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
        except Exception as e:
            print(f"Ошибка при парсинге: {e}")
            return None
    
    data_selector_for_dir = 'h2'

    parsed_data_for_dir = parse_numbers(url, data_selector_for_dir)

    dir = ""

    if parsed_data_for_dir:
        for item in parsed_data_for_dir:
            dir = item.get_text().split()[0]
    
    print(dir)

    data_selector_for_numbers = '.RatingPage_rating__OrcOU'

    parsed_data_for_numbers = parse_numbers(url, data_selector_for_numbers)

    find = ""

    num_bvi_kv  = -1
    num_all_kv = -1
    num_cel_kv = -1
    num_osob_kv = -1
    num_otdel_kv = -1

    if parsed_data_for_numbers:
        for item in parsed_data_for_numbers:
            find = item.get_text()

        try:
            ind_bvi_kv = find.index("Без вступительных испытаний") + len("Без вступительных испытаний")
            num_bvi_kv = int(find[ind_bvi_kv:ind_bvi_kv + 10].split()[0])
            print(f'Номер первого бви: {num_bvi_kv}')
        except ValueError:
            print("Никто не участвует в конкурсе бви")

        try:
            ind_cel_kv = find.index("Целевая квота") + len("Целевая квота")
            num_cel_kv = int(find[ind_cel_kv:ind_cel_kv + 10].split()[0])
            print(f'Номер первой целевой квоты: {num_cel_kv}')
        except ValueError:
            print("Никто не участвует в конкурсе целевой квоты")

        try:
            ind_osob_kv = find.index("Особая квота") + len("Особая квота")
            num_osob_kv = int(find[ind_osob_kv:ind_osob_kv + 10].split()[0])
            print(f'Номер первой особой квоты: {num_osob_kv}')
        except ValueError:
            print("Никто не участвует в конкурсе особой квоты")
        
        try:
            ind_otdel_kv = find.index("Отдельная квота") + len("Отдельная квота")
            num_otdel_kv = int(find[ind_otdel_kv:ind_otdel_kv + 10].split()[0])
            print(f'Номер первой отдельной квоты : {num_otdel_kv}')
        except ValueError:
            print("Никто не участвует в конкурсе отдельной квоты")
        
        try:
            ind_all_kv = find.index("Общий конкурс") + len("Общий конкурс")
            num_all_kv = int(find[ind_all_kv:ind_all_kv + 10].split()[0])
            print(f'Номер первой общей квоты : {num_all_kv}')
        except ValueError:
            print("Никто не участвует в общем конкрусе")
        
    else:

        print(parsed_data_for_numbers, [num_bvi_kv, num_all_kv, num_cel_kv, num_osob_kv, num_otdel_kv])

    data_selector_all = '.RatingPage_table__item__qMY0F'
    parsed_data_all = parse_all(url, data_selector_all)

    if parsed_data_all:
        for item in parsed_data_all:
            find = item.get_text()
            
            user_num = int(find.split()[0])
            try:
                user_id = int(find[find.index("№") + 1:find.index("№") + 8])
            except ValueError:
                continue
            
            bool_bvi_kv  = False
            bool_cel_kv = False
            bool_osob_kv = False
            bool_otdel_kv = False
            bool_all_kv = False        

            if num_bvi_kv != -1 and user_num >= num_bvi_kv:
                if num_cel_kv != -1:
                    if user_num < num_cel_kv:
                        bool_bvi_kv = True
                elif num_osob_kv != -1:
                    if user_num < num_osob_kv:
                        bool_bvi_kv = True
                elif num_otdel_kv != -1:
                    if user_num < num_otdel_kv:
                        bool_bvi_kv = True
                elif num_all_kv != -1:
                    if user_num < num_all_kv:
                        bool_bvi_kv = True
                else:
                    bool_bvi_kv = True

            if num_cel_kv != -1 and user_num >= num_cel_kv:
                if num_osob_kv != -1:
                    if user_num < num_osob_kv:
                        bool_cel_kv = True
                elif num_otdel_kv != -1:
                    if user_num < num_otdel_kv:
                        bool_cel_kv = True
                elif num_all_kv != -1:
                    if user_num < num_all_kv:
                        bool_cel_kv = True
                else:
                    bool_cel_kv = True
                
            if num_osob_kv != -1 and user_num >= num_osob_kv:
                if num_otdel_kv != -1:
                    if user_num < num_otdel_kv:
                        bool_osob_kv = True
                elif num_all_kv != -1:
                    if user_num < num_all_kv:
                        bool_osob_kv = True
                else:
                    bool_osob_kv = True
            
            if num_otdel_kv != -1 and user_num >= num_otdel_kv:
                if num_all_kv != -1:
                    if user_num < num_all_kv:
                        bool_otdel_kv = True
                else:
                    bool_otdel_kv = True
            
            if num_all_kv != -1 and user_num >= num_all_kv:
                bool_all_kv = True
                
            if bool_bvi_kv:

                priority = int(find[find.index("Олимпиада")-3:find.index("Олимпиада")].split()[-1])
                id_sum = int(find[find.index("Основной")-2:find.index("Основной")].split()[-1])
                entr_ex = 0
                
                user_inf = str(user_id) + " Без-вступительных-испытаний " + str(priority) + " " + str(id_sum) + " " + str(entr_ex) + " " + '\n' 

                all_users_inf.append(user_inf)

            elif bool_cel_kv:

                priority = int(find[find.index("Вид")-3:find.index("Вид")].split()[-1])
                try:
                    id_sum = int(find[find.index("Балл")-2:find.index("Балл")].split()[-1])
                except:
                    try:
                        find.index("Без прохождения вступительных испытаний")
                        id_sum = 301
                    except:
                        id_sum = 0
                entr_ex = int(find[find.index("Преимущественное")-4:find.index("Преимущественное")].split()[-1])
                
                user_inf = str(user_id) + " Целевая-квота " + str(priority) + " " + str(id_sum) + " " + str(entr_ex) + " " + '\n'

                all_users_inf.append(user_inf)

            elif bool_osob_kv:

                priority = int(find[find.index("Вид")-3:find.index("Вид")].split()[-1])
                try:
                    id_sum = int(find[find.index("Балл")-2:find.index("Балл")].split()[-1])
                except ValueError:
                    try:
                        find.index("Без прохождения вступительных испытаний")
                        id_sum = 301
                    except:
                        id_sum = 0
                entr_ex = int(find[find.index("Преимущественное")-4:find.index("Преимущественное")].split()[-1])
                
                user_inf = str(user_id) + " Особая-квота " + str(priority) + " " + str(id_sum) + " " + str(entr_ex) + " " + '\n'

                all_users_inf.append(user_inf)

            elif bool_otdel_kv:

                priority = int(find[find.index("Вид")-3:find.index("Вид")].split()[-1])
                try:
                    id_sum = int(find[find.index("Балл")-2:find.index("Балл")].split()[-1])
                except ValueError:
                    try:
                        find.index("Без прохождения вступительных испытаний")
                        id_sum = 301
                    except:
                        id_sum = 0
                entr_ex = int(find[find.index("Преимущественное")-4:find.index("Преимущественное")].split()[-1])
                
                user_inf = str(user_id) + " Отдельная-квота " + str(priority) + " " + str(id_sum) + " " + str(entr_ex) + " " + '\n'

                all_users_inf.append(user_inf)
            elif bool_all_kv:

                priority = int(find[find.index("Вид")-3:find.index("Вид")].split()[-1])
                try:
                    id_sum = int(find[find.index("Балл")-2:find.index("Балл")].split()[-1])
                except ValueError:
                    id_sum = 0
                entr_ex = int(find[find.index("Преимущественное")-4:find.index("Преимущественное")].split()[-1])
                
                user_inf = str(user_id) + " Общий-конкурс " + str(priority) + " " + str(id_sum) + " " + str(entr_ex) + " " + '\n'

                all_users_inf.append(user_inf)

            else:
                print("ERROR")
    else:
        print(parsed_data_all, [num_bvi_kv, num_all_kv, num_cel_kv, num_osob_kv, num_otdel_kv], '\n')

    #Ввод данных в txt файл
    name =  uni + " " + dir + ".txt"
    f = open(name, "w")

    for i in all_users_inf:
        f.write(i)
    f.close()

    print("FINISH", '\n')

