FROM python:3.7.10

ENV APP_HOME /opt/sells-report

USER root
WORKDIR $APP_HOME
ENTRYPOINT ["python3"]
EXPOSE 8000

# 安装依赖
RUN mkdir -p $APP_HOME && \
    echo 'PS1="\[\e[32m\][\[\e[35m\]\u\[\e[m\]@\[\e[36m\]\h\[\e[31m\] \w\[\e[32m\]]\[\e[36m\]$\[\e[m\] "' >> /root/.bashrc

RUN pip3 install \
fastapi==0.61.1 \
uvicorn==0.11.8 \
pydantic==1.6.1 \
requests==2.24.0 \
httpx==0.14.3 \
PyYAML==5.3.1 \
pandas==1.2.0 \
numpy==1.19.5 \
xlwt==1.3.0 \
xlrd==2.0.1 \
python-multipart==0.0.5 \
openpyxl==3.0.3 \
aiofiles==0.6.0 \
PyYAML==5.3.1

COPY . $APP_HOME