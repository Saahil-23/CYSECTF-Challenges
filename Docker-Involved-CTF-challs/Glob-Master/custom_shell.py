#!/usr/bin/python3
import os
import sys

# Configuration
FORBIDDEN_CHARS = ["*", "?"]
FORBIDDEN_STRING = "flag_v3ry_sp3c1f1c_n4m3" 

print("=================================================")
print("Welcome to the Restricted Glob Shell.")
print(f"Your Goal: Read contents of {FORBIDDEN_STRING}")
print("Rules: No * or ? allowed. You cannot type the filename directly.")
print("=================================================")

while True:
    try:
        user_input = input("user@glob-challenge:~$ ").strip()

        if not user_input: continue
        if user_input in ["exit", "quit"]:
            break

        if any(c in user_input for c in FORBIDDEN_CHARS):
            print("Error: The characters * and ? are banned here!")
            continue

        if FORBIDDEN_STRING in user_input:
            print(f"Error: You are not allowed to type {FORBIDDEN_STRING} explicitly!")
            continue

        os.system(user_input)

    except (EOFError, KeyboardInterrupt):
        print("\nExiting...")
        break