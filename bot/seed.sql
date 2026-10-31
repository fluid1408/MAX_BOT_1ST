-- Очистка таблиц (на случай перезапуска)
DELETE FROM answers;
DELETE FROM buttons;

-- ГЛАВНОЕ МЕНЮ
INSERT INTO buttons (button_id, button_text, parent_menu, "order", is_active, button_type) VALUES
('my_group', 'Моя группа', 'main', 1, true, 'callback'),
('study_process', 'Организация учебного процесса', 'main', 2, true, 'callback'),
('electronic_resources', 'Доступ к электронно-информационным ресурсам', 'main', 3, true, 'callback'),
('tochka_kpenia', 'Университетская «Точка кипения»', 'main', 4, true, 'callback'),
('tracks', 'Треки развития для студентов', 'main', 5, true, 'callback'),
('vk_groups', 'Группы треков ВКонтакте', 'main', 6, true, 'callback');

-- ПОДМЕНЮ: УЧЕБНЫЙ ПРОЦЕСС
INSERT INTO buttons (button_id, button_text, parent_menu, "order", is_active, button_type) VALUES
('study_year_structure', 'Структура учебного года', 'study_process', 1, true, 'callback'),
('study_forms', 'Формы обучения', 'study_process', 2, true, 'callback'),
('study_classes', 'Учебные занятия', 'study_process', 3, true, 'callback'),
('study_assessment', 'Аттестация и оценки', 'study_process', 4, true, 'callback'),
('study_practices', 'Практики', 'study_process', 5, true, 'callback');

-- ПОДМЕНЮ: ЭИР
INSERT INTO buttons (button_id, button_text, parent_menu, "order", is_active, button_type) VALUES
('eir_how_to_get', 'Как получить логин и пароль', 'electronic_resources', 1, true, 'callback'),
('eir_rules', 'Правила и важная информация', 'electronic_resources', 2, true, 'callback'),
('eir_contacts', 'Куда обращаться', 'electronic_resources', 3, true, 'callback');

-- ПОДМЕНЮ: ТОЧКА КИПЕНИЯ
INSERT INTO buttons (button_id, button_text, parent_menu, "order", is_active, button_type) VALUES
('tochka_about', 'О центре', 'tochka_kpenia', 1, true, 'callback'),
('tochka_team', 'Команда и контакты', 'tochka_kpenia', 2, true, 'callback'),
('tochka_infrastructure', 'Посмотреть инфраструктуру', 'tochka_kpenia', 3, true, 'link'),
('tochka_events', 'Провести мероприятие', 'tochka_kpenia', 4, true, 'link'),
('tochka_calendar', 'Календарь мероприятий', 'tochka_kpenia', 5, true, 'link');

-- ПОДМЕНЮ: ТРЕКИ ВК
INSERT INTO buttons (button_id, button_text, parent_menu, "order", is_active, button_type) VALUES
('track_culture', 'Культура и творчество', 'vk_groups', 1, true, 'link'),
('track_science', 'Наука и инновации', 'vk_groups', 2, true, 'link'),
('track_sport', 'ЗОЖ и спорт', 'vk_groups', 3, true, 'link'),
('track_volunteer', 'Волонтерство и соц. проектирование', 'vk_groups', 4, true, 'link'),
('track_leadership', 'Лидерство и управление', 'vk_groups', 5, true, 'link'),
('track_business', 'Бизнес и предпринимательство', 'vk_groups', 6, true, 'link'),
('track_career', 'Профессионализм и карьера', 'vk_groups', 7, true, 'link');

-- ОТВЕТЫ (тексты в одну строку, без переносов, кавычки внутри текста убраны)
INSERT INTO answers (button_id, answer_text, answer_type, is_active) VALUES
('my_group', 'Информация о вашей группе будет здесь позже.', 'text', true),
('tracks', 'Если за период обучения ты хочешь сформировать универсальные умения (компетенции), чтобы повысить свою ценность на рынке труда, стань участником треков личностного и профессионального развития!', 'text', true),
('study_year_structure', 'Учебный год начинается 1 сентября и состоит из двух семестров: осеннего и весеннего. • Осенний семестр: сентябрь-январь. • Зимние каникулы: январь-февраль (~2 недели). • Весенний семестр: февраль-июнь. • Летние каникулы: ~2 месяца.', 'text', true),
('study_forms', 'Формы обучения: очная, очно-заочная (вечерняя) и заочная. Сроки обучения (бакалавриат): очная — 4-5 лет, очно-заочная/заочная — 4,5-5,5 лет.', 'text', true),
('study_classes', 'Занятия проводятся по расписанию. Академический час — 45 минут (пара — 1,5 часа). Перерыв — 10 минут, обед — не менее 45 минут. Максимальная нагрузка — 54 академических часа в неделю.', 'text', true),
('study_assessment', 'Применяется балльно-рейтинговая система. Экзамены оцениваются «отлично», «хорошо», «удовлетворительно», «неудовлетворительно». Зачёты — «зачтено» / «не зачтено».', 'text', true),
('study_practices', 'Учебная и производственная практики осуществляются на основе договоров с предприятиями и организациями.', 'text', true),
('eir_how_to_get', 'Логин и пароль приходят смс-оповещением на номер, указанный при поступлении. При авторизации добавляй @chsu.ru.', 'text', true),
('eir_rules', 'Сохраняй смс с логинами и паролями! Если не получил смс — обратись в личный кабинет студента или Единый деканат.', 'text', true),
('eir_contacts', 'Обращайся в Единый деканат.', 'text', true),
('tochka_about', 'Центр коллективной работы «Точка кипения» создан в 2019 году. Ежегодно проводится более 200 мероприятий.', 'text', true),
('tochka_team', 'Контакты: • Адрес: ул. М. Горького 14 • Тел.: +7 (8202) 55-26-81 • E-mail: tochkakipenia@chsu.ru', 'text', true);

-- ССЫЛКИ
INSERT INTO answers (button_id, answer_text, answer_type, media_url, is_active) VALUES
('tochka_infrastructure', 'Посмотреть инфраструктуру', 'link', 'https://leader-id.ru/places/1038', true),
('tochka_events', 'Провести мероприятие', 'link', 'https://vk.com/tkchsu', true),
('tochka_calendar', 'Календарь мероприятий', 'link', 'https://leaderid.ru/events?actual=1&cityId=1169112&registrationActual=1&sort=date', true),
('track_culture', '', 'link', 'https://vk.ru/art_chsu', true),
('track_science', '', 'link', 'https://vk.ru/naukachsu35', true),
('track_sport', '', 'link', 'https://vk.ru/publiczdorovyiychsu35', true),
('track_volunteer', '', 'link', 'https://vk.ru/volonterchsu', true),
('track_leadership', '', 'link', 'https://vk.ru/liderchsu35', true),
('track_business', '', 'link', 'https://vk.ru/business_chsu', true),
('track_career', '', 'link', 'https://vk.ru/rabotachsu', true);