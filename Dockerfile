FROM python:3.10.12

ENV APP_HOME /opt/sells-report

USER root
WORKDIR $APP_HOME
ENTRYPOINT ["python3"]
EXPOSE 8000

# 安装依赖
RUN mkdir -p $APP_HOME && \
    echo 'PS1="\[\e[32m\][\[\e[35m\]\u\[\e[m\]@\[\e[36m\]\h\[\e[31m\] \w\[\e[32m\]]\[\e[36m\]$\[\e[m\] "' >> /root/.bashrc

RUN pip3 install \
fastapi==0.109.1 \
uvicorn==0.23.1 \
PyYAML==6.0.1 \
pandas==2.2.2 \
numpy==2.0.0 \
pytz==2024.1 \
tzdata==2024.1 \
openpyxl==3.1.5 \
et-xmlfile==1.1.0 \
python-multipart==0.0.9

COPY . $APP_HOME