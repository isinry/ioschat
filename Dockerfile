FROM python:3.10.5

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器的工作目录中
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN export PYTHONIOENCODING=utf-8

# 设置环境变量（根据实际应用进行调整）
ENV PYTHONIOENCODING=utf-8
ENV OPENAI_API_BASE_URL=
ENV OPENAI_API_KEY=
ENV PROMPT=

# （可选）暴露应用端口
EXPOSE 3026

# 定义启动命令，使用Gunicorn启动Flask应用
CMD ["python", "app.py"]