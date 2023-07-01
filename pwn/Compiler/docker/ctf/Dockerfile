FROM ubuntu:20.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd python3 && \
    apt-get -y install cron

COPY clean-cron /etc/cron.d/clean-cron
RUN chmod 0644 /etc/cron.d/clean-cron
RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/clean-cron
CMD cron && tail -f /var/log/cron.log

RUN useradd -m ctf

WORKDIR /home/ctf

RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

COPY ./bin/ /home/ctf/

RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chmod 750 /home/ctf/trans_asm && \
    chmod 750 /home/ctf/trans_IR && \
    chmod 760 /home/ctf/test.c && \
    chmod 760 /home/ctf/inter.txt && \
    mv /home/ctf/flag /flag && \
    chmod 740 /flag && \
    chmod 740 /home/ctf/server.py 
    
CMD ["/start.sh"]

EXPOSE 9999
