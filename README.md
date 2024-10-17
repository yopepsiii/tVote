![tVote](https://i.ibb.co/5x24Qt9/Frame-12.png)

## Т-Голосование
Платформа для онлайн-голосований за кандидатов, созданная для решения проблем оффлайн-голосований. Расчитана на небольшое кол-во пользователей.  

## Что было интересно  
**Войти через Google:** Задумывалась реализация Google OpenID, но пришлось отказаться от этой идеи, т.к. времени на реализацию проекта не хватало. В планах также был вход и через другие различные платформы.  

**Mailersend:** Это сервис для автоматической рассылки писем на почты при выдаче доступа к платформе новому человеку. Он полностью реализован в проекте, вам нужно просто указать свой API-ключ и домен от сервиса.  

**Управление через API:** Задумывалась админ-панель, но остановился на управление через запросы к API (документация `/docs`), все также из-за сжатых сроков. Достаточно создать аккаунт владельца внутри бд для доступа к всем эндпоинтам.  

**Тесты:** Написал юнит-тесты для backend'a через *pytest*.  

**Сгенерированные SSL-сертификаты для localhost:** Тестировал работу ssl-сертификатов, поэтому сгенерируйте новые сертификаты для `localhost` или перепишите `nginx.conf`  
1. Перейдите из корневой дирректории в `nginx/dev/cert`
2. Сгенерируйте новые сертификаты:
```bash
openssl req -x509 -out localhost.crt -keyout localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
```
3. Начинайте установку

### Установка
1. Склонируйте репозиторий:
```bash
git clone https://github.com/ваш_пользователь/ваш_репозиторий.git
```  
2. Установите [Docker](https://www.docker.com/products/docker-desktop/)  
3. Создайте в корневой дирректории .env и заполните в соответствии с файлом `config.py`
```python
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    owner_email: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    google_client_id: str
    google_client_secret: str
    ms_api_key: str
    ms_domain: str
```
4. Запустите проект локально через `docker compose`:
```bash
docker compose -f docker-compose-dev.yml up -d
```
5. Откройте документацию: `https://localhost/api/v1/docs`
