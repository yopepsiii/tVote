# 1. Указываем базовый образ
FROM node:18-alpine

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/tVote/frontend

# 3. Копируем package.json и package-lock.json для установки зависимостей
COPY package*.json ./

# 4. Устанавливаем зависимости
RUN npm install

# 5. Копируем все остальные файлы в контейнер
COPY . .

# 6. Собираем production-сборку
RUN npm run build

# 7. Указываем рабочую директорию для работы с файлами сборки
WORKDIR /app/build

# 8. Команда по умолчанию
CMD ["npm", "start"]
