### Инфо
Исходный код: https://github.com/TeaDove/evraz-hack-misis-anime <br>
Демо видео: https://drive.google.com/file/d/1P48-pA65rloAXaj0YoXIH8gnvUF-sTm6/view?usp=share_link <br>
Интерфейс: https://more-tech-test-sdkjf2.website.yandexcloud.net/ <br>
Бекенд: https://kodiki-hack.ru:8000/rapidoc (сваггер)<br>
Презентация: https://docs.google.com/presentation/d/1QAJ6SP_N2Q5dC_xDfNEl-xDTfyyHn_b7LaKz0dl4J_o/edit?usp=sharing <br>

### Алгоритм работы предсказаний
Алгоритм работы предсказаний:<br>

### Дополнительно
#### Поиск выбросов:
Если какое-либо из температурных полей больше 1000, либо меньше -100 градусов Цельсия, то оно помечается как выброс(outliner) и зануляется, то есть проставляется как null.

### Доступ
Фронтенд сайт доступен по http://158.160.13.117 <br>
Swagger доступен по http://158.160.13.117:8000/docs <br>
Графана: http://158.160.13.117:3000/d/PZHmNE1Vk/main-copy?orgId=1&kiosk=&from=now-12h&to=now <br>

### Запуск
- backend:
```bash
cd backend
docker-compose up
```
- frontend:
```bash
cd frontend
yarn install && yarn dev --host=10.129.0.25 --port=80
```
- Все сразу: (пока не работает, запускайте бекенд и фронтенд отдельно)
```bash
docker-compose up
```

### Нагрузочное тестирование
Тесты:
- 5 пользователей, 1 минута тестирования, 20 PRS: 420ms - P95%
- 100 пользователей, 1 минута тестирования, 50 PRS: 1.4s - P95%
В случае отсутствия  большой нагрузки все запросы в среднем обрабатываются за 300мс. <br>
В случае нагрузки, поставляемой 100 пользователей, средний ответ составляет 1.4c, при нагрузке 50 запросов в секунду.<br>
Ниже представление схемы тестирования на 5 пользователях, 20PRS.
![loadtest_1](./loadtests_1.png)
![loadtest_2](./loadtests_2.png)
