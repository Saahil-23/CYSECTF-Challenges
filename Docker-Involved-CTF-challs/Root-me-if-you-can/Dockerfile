# Base image
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install SSH, at, sudo, supervisor, and required tools
RUN apt-get update && apt-get install -y \
    openssh-server sudo supervisor at \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create SSH user and set password
RUN useradd -m -s /bin/bash user && echo "user:StrongP@ssw0rd" | chpasswd

# Add flag in user's home
RUN echo "FLAG{user_level_ssh_flag}" > /home/user/flag.txt && \
    chown user:user /home/user/flag.txt && chmod 600 /home/user/flag.txt

# Add root-only flag
RUN echo "FLAG{root_level_priv_esc_success}" > /root/root.txt && chmod 600 /root/root.txt

# Grant user sudo rights ONLY to `at`
RUN echo "user ALL=(ALL) NOPASSWD: /usr/bin/at" > /etc/sudoers.d/at-only
RUN chmod 440 /etc/sudoers.d/at-only

# Fix `at` by ensuring the daemon is enabled
RUN mkdir -p /var/spool/cron/atjobs /var/spool/cron/atspool && \
    chmod 700 /var/spool/cron/atjobs && \
    chmod 700 /var/spool/cron/atspool && \
    chown daemon:daemon /var/spool/cron/atjobs /var/spool/cron/atspool

# Configure SSH to allow password auth and disable root login
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    echo "AllowUsers user" >> /etc/ssh/sshd_config

# Create SSH runtime directory
RUN mkdir -p /var/run/sshd

# Copy Supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose SSH port
EXPOSE 22

# Start SSH and atd via Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
