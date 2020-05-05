FROM python:3.7
MAINTAINER Eduard Asriyan <ed-asriyan@protonmail.com>

WORKDIR /application

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD main.py .
ADD m4m_gsm.py .
ADD m4m_imu.py .
ADD m4m_obd.py .
ADD m4m_utils.py .

CMD python main.py
