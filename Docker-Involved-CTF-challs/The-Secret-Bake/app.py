#!/usr/bin/env python3
from flask import Flask, render_template_string, send_file, make_response
import os
from datetime import datetime

app = Flask(__name__)

# Read the flag
def get_flag():
    try:
        with open('flag.txt', 'r') as f:
            return f.read().strip()
    except:
        return "CTF{COOKIE_MONSTER_DEBUG_FLAG}"

# Minimal HTML template with just the cookie image and recipe
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grandma's Cookie Recipe</title>
    <style>
        body {
            font-family: 'Georgia', serif;
            background-color: #f5f5dc;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #8B4513;
            text-align: center;
            border-bottom: 2px solid #8B4513;
            padding-bottom: 10px;
        }
        .cookie-img {
            max-width: 400px;
            display: block;
            margin: 20px auto;
            border-radius: 10px;
        }
        .recipe {
            line-height: 1.6;
        }
        .ingredients, .instructions {
            margin: 20px 0;
        }
        ul, ol {
            margin-left: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍪 Grandma's Secret Chocolate Chip Cookie Recipe</h1>
        
        <img src="/static/cookie.jpg?version=1" alt="Delicious Chocolate Chip Cookie" class="cookie-img">
        
        <div class="recipe">
            <div class="ingredients">
                <h2>Ingredients:</h2>
                <ul>
                    <li>2 ¼ cups all-purpose flour</li>
                    <li>1 teaspoon baking soda</li>
                    <li>1 teaspoon salt</li>
                    <li>1 cup butter, softened</li>
                    <li>¾ cup granulated sugar</li>
                    <li>¾ cup packed brown sugar</li>
                    <li>2 large eggs</li>
                    <li>2 teaspoons vanilla extract</li>
                    <li>2 cups chocolate chips</li>
                </ul>
            </div>
            
            <div class="instructions">
                <h2>Instructions:</h2>
                <ol>
                    <li>Preheat oven to 375°F (190°C)</li>
                    <li>In a small bowl, mix flour, baking soda, and salt</li>
                    <li>In a large bowl, beat butter and sugars until creamy</li>
                    <li>Add eggs one at a time, then add vanilla</li>
                    <li>Gradually beat in flour mixture</li>
                    <li>Stir in chocolate chips</li>
                    <li>Drop by rounded tablespoons onto ungreased baking sheets</li>
                    <li>Bake for 9-11 minutes or until golden brown</li>
                    <li>Cool on baking sheets for 2 minutes; remove to wire racks</li>
                </ol>
            </div>
            
            <p><em>Makes about 4 dozen cookies. Perfect for sharing with friends!</em></p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page that sets the cookie with the flag"""
    flag = get_flag()
    
    # Create response with HTML
    response = make_response(render_template_string(HTML_TEMPLATE))
    
    # Set cache control headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # Set ONLY the flag cookie (no decoy cookies)
    response.set_cookie(
        'flag', 
        flag,
        httponly=False,
        secure=False,
        samesite='Lax'
    )
    
    return response

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files with cache control"""
    try:
        response = send_file(f'static/{filename}')
        response.headers['Cache-Control'] = 'no-cache, must-revalidate'
        return response
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    print("🍪 The Secret Bake CTF Challenge starting...")
    print("🔑 Flag will be set in a cookie named 'flag'")
    print("🌐 Server running on http://0.0.0.0:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=False)