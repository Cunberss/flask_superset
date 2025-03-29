FROM python:3.11-slim

WORKDIR /project

COPY . /project/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/project/superset"

EXPOSE 5000

CMD alembic upgrade head && python3 superset/src/db/seed.py && python3 superset/src/main.py

