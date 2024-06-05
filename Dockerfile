FROM python:3.11 AS builder

WORKDIR /build

COPY spaceinvaders/requirements.txt .

RUN pip install -r requirements.txt

COPY spaceinvaders/ .

RUN pygbag --build main.py

WORKDIR /web

RUN cp -r /build/build/web/* /web/

RUN sed -i 's/<html lang="en-us">/<html lang="en-us"><script src="\/loadToken.js"><\/script><script src="\/loadAnalyticsMethods.js"><\/script><script src="\/loadConfig.js"><\/script>/' index.html

COPY spaceinvaders/loadToken.js .
COPY spaceinvaders/loadAnalyticsMethods.js .
COPY spaceinvaders/loadConfig.js .

FROM afonsopc/web-server AS runtime

COPY --from=builder /web/ /web/