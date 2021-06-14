FROM python:3.9

WORKDIR /usr/local/src

# Copy code
COPY . .

# Don't use a virtualenv
# ARG POETRY_VIRTUALENVS_CREATE=False

# Upgrade pip and install dependencies
RUN pip install --upgrade pop && pip install -r requirements.txt
# RUN pip install --upgrade pip \
#     && pip install poetry \
#     && poetry install --no-dev