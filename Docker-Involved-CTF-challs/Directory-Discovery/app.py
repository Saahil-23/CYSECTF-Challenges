#!/usr/bin/env python3
from flask import Flask, render_template_string
import base64

app = Flask(__name__)

# HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Corporate Site</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        header {
            background: #2c3e50;
            color: white;
            padding: 20px 0;
            text-align: center;
        }
        .content {
            padding: 40px 20px;
            line-height: 1.6;
        }
        .footer {
            text-align: center;
            padding: 20px;
            margin-top: 40px;
            border-top: 1px solid #eee;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Acme Corporation</h1>
            <p>Innovating Tomorrow, Today</p>
        </header>
        
        <div class="content">
            <h2>Welcome to Acme Corporation</h2>
            <p>We are a leading provider of innovative solutions for businesses worldwide. Our team of experts is dedicated to delivering cutting-edge technology and exceptional service.</p>
            
            <h3>About Us</h3>
            <p>Founded in 1995, Acme Corporation has been at the forefront of technological innovation. Our mission is to empower businesses through reliable and scalable solutions.</p>
            
            <h3>Our Services</h3>
            <ul>
                <li>Web Development & Design</li>
                <li>Cloud Infrastructure</li>
                <li>Cybersecurity Solutions</li>
                <li>Digital Transformation</li>
            </ul>
            
            <h3>Contact Information</h3>
            <p>Email: info@acme-corp.com<br>
            Phone: (555) 123-4567<br>
            Address: 123 Business Ave, Suite 100</p>
        </div>
        
        <div class="footer">
            <p>&copy; 2024 Acme Corporation. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

# The flag to be encoded - using the recommended leet flag
FLAG = "SAKEC{H1DD3N_D1R_D3C0D3R}"

@app.route('/')
def index():
    """Main corporate website page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/6769')
def hidden_directory():
    """Hidden directory with encoded flag"""
    # Encode the flag in multiple layers to make it more challenging
    encoded_flag = base64.b64encode(FLAG.encode()).decode()
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Configuration File</title>
    <style>
        body {{ font-family: monospace; background: #1a1a1a; color: #00ff00; padding: 20px; }}
        .file-content {{ background: #000; padding: 20px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>System Configuration Backup</h1>
    <div class="file-content">
        <pre>
# System Configuration Backup
# Generated: 2024-01-15 14:30:22
# Do not modify manually

backup_checksum: {encoded_flag}
system_id: ACME-SRV-6769
last_updated: 2024-01-15T14:30:22Z
status: ACTIVE

# This file contains encoded system parameters
# for internal use only
        </pre>
    </div>
    <p><em>This appears to be a system configuration backup file.</em></p>
</body>
</html>
"""

@app.route('/robots.txt')
def robots():
    """Robots.txt file - common place to check"""
    return "User-agent: *\nDisallow: /admin\nDisallow: /backup\nDisallow: /6769\n\n# Nothing to see here..."

@app.route('/.gitignore')
def gitignore():
    """Gitignore file - another common check"""
    return "# Ignore system files\n*.log\n*.tmp\n\n# Ignore backup directories\n/backups/"

if __name__ == '__main__':
    print("🚀 Hidden Directory CTF Challenge starting...")
    print("🔍 Hidden directory: /6769")
    print("🔑 Flag encoded in base64 within the hidden directory")
    print("🌐 Server running on http://0.0.0.0:9676")
    
    app.run(host='0.0.0.0', port=9676, debug=False)