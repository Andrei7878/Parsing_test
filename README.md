# Parsing_test
1. Создаем файл со всеми необходимыми библиотеками
2. Импортируем библиотеки
3. Прописываем необходимые константы с названием файла и адреса парсинга страницы, а также указываем агент браузера
4. Прописываем функции с применением библиотеки bs4. В первой достаем ссылки на товары по определенным тегам, а во второй конкретно переходим по ссылкам и достаем из кода
html о тегам необходимые нам наименования и картинки и записываем их в список словарей.
5. Создаем функцию записи информации в файл csv с помощью модуля csv. Записываем ключи как названия столбцов а строки значения ключей.
6. Настраиваем пагинацию, то есть необходимое колиство страниц для парсинга, вводится пользователем и запускаем парсер, прописав предварительно запрос на сервер и все 
7. необходимые нам фукции.
