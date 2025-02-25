# WhatsApp FAQ Bot (no LLM)

Бот використовує FAISS для пошуку найкращих відповідей і SentenceTransformer для кодування тексту.

## Передумови
1. **Overview & Setup**: Begin your journey [here](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
2. Create [System User Access Tokens](https://developers.facebook.com/docs/whatsapp/business-management-api/get-started#system-user-access-tokens)
## Функціонал
- Обробка запитів через WhatsApp API
- Пошук відповідей за допомогою FAISS
- Кешування відповідей у Redis

## Встановлення та запуск через Docker
### 1. Клонування репозиторію
```sh
git clone https://github.com/evgenidzze/whatsapp_faq
cd whatsapp_faq
```

### 2. Створення файлу `.env`
Створи `.env` у кореневій директорії та додай необхідні змінні оточення:
```env
PHONE_NUMBER_ID=your_phone_number_id (This is your WhatsApp ID, i.e., phone number. Make sure it is added to the account as shown in the example test message.)
ACCESS_TOKEN=your_system_access_token (Get after creating System User Access Token)
APP_ID="<YOUR-WHATSAPP-BUSINESS-APP_ID>" (Found at App Dashboard)
REDIS_HOST=redis
```

### 3. Запуск docker compose
```sh
docker compose up -d --build
```

## Використання ngrok для доступу до локального FastAPI ззовні
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

### 3. Встановити webhook
- [Інструкція](https://developers.facebook.com/docs/graph-api/webhooks/getting-started#configure-webhooks-product)