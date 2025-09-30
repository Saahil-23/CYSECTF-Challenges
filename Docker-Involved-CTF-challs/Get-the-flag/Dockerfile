# Use Ubuntu 22.04 as base
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install vsftpd and tools
RUN apt-get update && apt-get install -y vsftpd dos2unix && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create ftpuser with password
RUN useradd -m -s /bin/bash ftpuser && echo "ftpuser:StrongPass123" | chpasswd

# Setup anonymous FTP folder with credentials file
RUN mkdir -p /home/ftp/anonymous && \
    echo -e "username: ftpuser\npassword: StrongPass123" > /home/ftp/anonymous/usercreds.txt && \
    chown -R ftpuser:ftpuser /home/ftp/anonymous && chmod 755 /home/ftp/anonymous && \
    chmod 644 /home/ftp/anonymous/usercreds.txt

# Setup ftpuser home folder with flag
RUN mkdir -p /home/ftpuser && \
    echo "CYSE{ftp_success}" > /home/ftpuser/flag.txt && \
    chown -R ftpuser:ftpuser /home/ftpuser && chmod 700 /home/ftpuser && chmod 600 /home/ftpuser/flag.txt

# Copy vsftpd config
COPY vsftpd.conf /etc/vsftpd.conf
RUN dos2unix /etc/vsftpd.conf

# Create required runtime directory for vsftpd
RUN mkdir -p /var/run/vsftpd/empty && chmod 755 /var/run/vsftpd/empty

# Expose FTP ports (control + passive)
EXPOSE 21 30000-30009

# Start vsftpd
CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]
