# Base image
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install SSH and Python3
RUN apt-get update && apt-get install -y \
    openssh-server python3 coreutils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 1. Setup SSH Daemon
RUN mkdir -p /var/run/sshd
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

# 2. Install the Custom Shell using Base64
# This prevents ALL escaping and newline errors
RUN echo "IyEvdXNyL2Jpbi9weXRob24zCmltcG9ydCBvcwppbXBvcnQgc3lzCgojIENvbmZpZ3VyYXRpb24KRk9SQklEREVOX0NIQVJTID0gWyIqIiwgIj8iXQpGT1JCSURERU5fU1RSSU5HID0gImZsYWdfdjNyeV9zcDNjMWYxY19uNG0zIgoKcHJpbnQoIj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0iKQpwcmludCgiV2VsY29tZSB0byB0aGUgUmVzdHJpY3RlZCBHbG9iIFNoZWxsLiIpCnByaW50KGYiWW91ciBHb2FsOiBSZWFkIGNvbnRlbnRzIG9mIHtGT1JCSURERU5fU1RSSU5HfSIpCnByaW50KCJSdWxlczogTm8gKiBvciA/IGFsbG93ZWQuIFlvdSBjYW5ub3QgdHlwZSB0aGUgZmlsZW5hbWUgZGlyZWN0bHkuIikKcHJpbnQoIj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0iKQoKd2hpbGUgVHJ1ZToKICAgIHRyeToKICAgICAgICB1c2VyX2lucHV0ID0gaW5wdXQoInVzZXJAZ2xvYi1jaGFsbGVuZ2U6fiQgIikuc3RyaXAoKQoKICAgICAgICBpZiBub3QgdXNlcl9pbnB1dDogY29udGludWUKICAgICAgICBpZiB1c2VyX2lucHV0IGluIFsiZXhpdCIsICJxdWl0Il06CiAgICAgICAgICAgIGJyZWFrCgogICAgICAgIGlmIGFueShjIGluIHVzZXJfaW5wdXQgZm9yIGMgaW4gRk9SQklEREVOX0NIQVJTKToKICAgICAgICAgICAgcHJpbnQoIkVycm9yOiBUaGUgY2hhcmFjdGVycyAqIGFuZCA/IGFyZSBiYW5uZWQgaGVyZSEiKQogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBpZiBGT1JCSURERU5fU1RSSU5HIGluIHVzZXJfaW5wdXQ6CiAgICAgICAgICAgIHByaW50KGYiRXJyb3I6IFlvdSBhcmUgbm90IGFsbG93ZWQgdG8gdHlwZSB7Rk9SQklEREVOX1NUUklOR30gZXhwbGljaXRseSEiKQogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBvcy5zeXN0ZW0odXNlcl9pbnB1dCkKCiAgICBleGNlcHQgKEVPRkVycm9yLCBLZXlib2FyZEludGVycnVwdCk6CiAgICAgICAgcHJpbnQoIlxuRXhpdGluZy4uLiIpCiAgICAgICAgYnJlYWsK" | base64 -d > /usr/local/bin/custom_shell.py

# Make it executable
RUN chmod +x /usr/local/bin/custom_shell.py

# 3. Create the User (Set shell to our custom script)
RUN useradd -m -d /home/user -s /usr/local/bin/custom_shell.py user && \
    echo "user:guest" | chpasswd

# 4. Create the Real Flag and the Fake Flags
WORKDIR /home/user

RUN for i in $(seq 1 30); do \
        SUFFIX=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 8 | head -n 1); \
        echo "Keep looking..." > "flag_$SUFFIX"; \
    done

ENV TARGET_FILE="flag_v3ry_sp3c1f1c_n4m3"
RUN echo "SAKEC{br4ck3ts_4r3_th3_k3y_t0_gl0bb1ng}" > "$TARGET_FILE"

RUN echo "Your goal is to read the file named: $TARGET_FILE" > README.txt
RUN echo "BUT... my shell will not let you type that name, nor use '*' or '?'." >> README.txt
RUN echo "Good luck!" >> README.txt

# Fix Permissions
RUN chown -R user:user /home/user && \
    chmod 644 /home/user/flag_* && \
    chmod 644 /home/user/README.txt

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]