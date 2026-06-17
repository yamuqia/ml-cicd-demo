# 指定基础镜像
FROM python:3.11-slim

# 设置容器内部工作目录, 后面的 COPY、RUN、CMD 默认都在 /app 下执行
WORKDIR /app

# 设置环境变量, 禁止生成 pycache 文件, 并且让日志实时输出
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 复制依赖文件
COPY requirements.txt .

# 安装依赖, 使用 --no-cache-dir 选项不保留 pip 下载缓存减少镜像大小, 升级 pip 以确保使用最新版本
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 把本地的 app 和 models 目录复制到容器的 /app 目录下
COPY app/ app/
COPY models/ models/

# 创建非 root 用户 appuser 并将 /app 目录的所有权赋予该用户
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

# 切换到非 root 用户
USER appuser

# 声明容器监听的端口, 这里是 8000, 与 FastAPI 默认端口一致
EXPOSE 8000

# 设置健康检查, 每30秒检查一次, 超时时间为5秒, 启动后10秒开始检查, 失败重试3次
# 使用 curl 或 wget 替代 python 代码，更简洁且避免依赖问题
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

# 指定容器启动时执行的命令, 使用 uvicorn 启动 FastAPI 应用, 监听所有接口的 8000 端口
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]