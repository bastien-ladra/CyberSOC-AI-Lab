FROM python:3.14.7-slim-bookworm@sha256:9ab8d9c8514b44f90cf0029dd42fdd7e9e211e639c8b995304cc04568dee900f

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    HOME=/home/app

RUN groupadd --gid 65532 app \
    && useradd --uid 65532 --gid app --create-home --home-dir /home/app --shell /usr/sbin/nologin app

COPY requirements.lock ./requirements.lock

RUN python -m pip install \
    --no-cache-dir \
    --require-hashes \
    -r requirements.lock \
    && python -m pip uninstall --yes setuptools wheel

COPY --chown=65532:65532 ai_assistant ./ai_assistant
COPY --chown=65532:65532 dashboard ./dashboard
COPY --chown=65532:65532 detection ./detection
COPY --chown=65532:65532 utils ./utils
COPY --chown=65532:65532 data ./data
COPY --chown=65532:65532 examples ./examples
COPY --chown=65532:65532 main.py ./main.py

USER 65532:65532

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=3)" || exit 1

CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
