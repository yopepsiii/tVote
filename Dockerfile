FROM python:3.12
COPY requirements.txt /usr/src/tVote/backend/requirements.txt
WORKDIR /usr/src/tVote/backend
RUN pip install -r requirements.txt
COPY . .

CMD sh -c "alembic upgrade head ; uvicorn app.main:app --host 0.0.0.0 --port 8000"