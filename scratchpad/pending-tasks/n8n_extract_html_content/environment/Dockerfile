FROM alpine:3.18

RUN apk add --no-cache python3 py3-pip jq nodejs npm

RUN adduser -D -s /bin/sh user
USER user
WORKDIR /home/user

COPY --chown=user:user workflow.json /home/user/workflow.json

CMD ["sleep", "infinity"]