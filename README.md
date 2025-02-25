# WhatsApp FAQ Bot (no LLM)

Бот використовує FAISS для пошуку найкращих відповідей і SentenceTransformer для кодування тексту.

## Функціонал
- Обробка запитів через WhatsApp API
- Пошук відповідей за допомогою FAISS
- Кешування відповідей у Redis

## Встановлення та запуск через Docker
### 1. Клонування репозиторію
```sh
git clone https://github.com/your-username/whatsapp-faq.git
cd whatsapp-faq
```

### 2. Створення файлу `.env`
Створи `.env` у кореневій директорії та додай необхідні змінні оточення:
```env
PHONE_NUMBER_ID=your_phone_number_id
ACCESS_TOKEN=your_access_token
REDIS_HOST=redis
```

### 3. Запуск контейнера
```sh
docker build -t whatsapp-faq .
docker run -p 8000:8000 --name whatsapp-faq -d whatsapp-faq
```

## Використання ngrok для доступу до FastAPI
Якщо ти хочеш протестувати API на локальному сервері з доступом зовні, можеш використовувати `ngrok`.

### 1. Встановлення ngrok (якщо не встановлено)
```sh
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
chmod +x ngrok
```

### 2. Запуск ngrok для перенаправлення трафіку на Docker-контейнер
```sh
./ngrok http 8000
```
Це створить публічний URL, наприклад:
```
Forwarding https://random-id.ngrok.io -> http://localhost:8000
```

Тепер можна використовувати `https://random-id.ngrok.io/docs` для доступу до FastAPI Swagger UI.

## Перевірка логів контейнера
Якщо контейнер не працює належним чином, перевір логи:
```sh
docker logs whatsapp-faq
```

## Зупинка та видалення контейнера
```sh
docker stop whatsapp-faq
docker rm whatsapp-faq
```

