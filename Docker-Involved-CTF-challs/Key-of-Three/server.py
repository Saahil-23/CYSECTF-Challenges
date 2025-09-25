#!/usr/bin/env python3
import socket
import subprocess
import os
import random
import re
import tempfile
import threading
from pathlib import Path

class ChmodChallenge:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 1337
        self.flag = self.read_flag()
        
    def read_flag(self):
        """Read the flag from file"""
        try:
            with open('flag.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return "FLAG{ERROR_CONTACT_ADMIN}"

    def generate_random_permissions(self):
        """Generate completely random UNIX permissions"""
        # Generate random octal (0-7) for user, group, others
        user_perm = random.randint(0, 7)
        group_perm = random.randint(0, 7)
        other_perm = random.randint(0, 7)
        
        octal_code = f"{user_perm}{group_perm}{other_perm}"
        
        # Convert to symbolic representation
        perm_string = self.octal_to_symbolic(octal_code)
        
        return perm_string, octal_code

    def octal_to_symbolic(self, octal):
        """Convert octal permission to symbolic notation"""
        if len(octal) != 3:
            return "invalid"
            
        permission_map = {
            '0': '---', '1': '--x', '2': '-w-', '3': '-wx',
            '4': 'r--', '5': 'r-x', '6': 'rw-', '7': 'rwx'
        }
        
        user, group, other = octal[0], octal[1], octal[2]
        return permission_map[user] + permission_map[group] + permission_map[other]

    def symbolic_to_octal(self, symbolic):
        """Convert symbolic permission to octal"""
        if len(symbolic) != 9:
            return None
            
        reverse_map = {
            '---': '0', '--x': '1', '-w-': '2', '-wx': '3',
            'r--': '4', 'r-x': '5', 'rw-': '6', 'rwx': '7'
        }
        
        try:
            user = symbolic[0:3]
            group = symbolic[3:6]
            other = symbolic[6:9]
            return reverse_map[user] + reverse_map[group] + reverse_map[other]
        except KeyError:
            return None

    def parse_chmod_command(self, command, filename):
        """Parse various chmod command formats and return intended permissions"""
        command = command.strip()
        
        # Remove multiple spaces and split
        parts = re.sub(r'\s+', ' ', command).split()
        
        if len(parts) < 2:
            return None, "Command too short"
            
        if parts[0].lower() != 'chmod':
            return None, "Not a chmod command"
        
        # Extract mode and handle options
        mode_arg = parts[1]
        
        # Case 1: Octal mode (e.g., 755, 0644, 4755)
        if re.match(r'^[0-7]{3,4}$', mode_arg):
            # If 4 digits, take last 3
            octal_mode = mode_arg[-3:]
            return octal_mode, "octal"
        
        # Case 2: Symbolic mode (e.g., u+x, g=rw, o-w, a=rx)
        elif any(c in mode_arg for c in ['u', 'g', 'o', 'a', '+', '-', '=']):
            # This is complex - we'll execute and check result
            return "symbolic", "symbolic"
        
        # Case 3: Verbose mode (e.g., +x, -w)
        elif mode_arg.startswith('+') or mode_arg.startswith('-'):
            return "symbolic", "symbolic"
        
        else:
            return None, "Unrecognized chmod format"

    def execute_chmod_safely(self, command, filename):
        """Execute chmod command safely with timeout"""
        try:
            # Use shell but with limited environment
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,  # 5 second timeout
                cwd='/tmp',  # Run in temp directory
                env={'PATH': '/bin:/usr/bin'}  # Limited PATH
            )
            return result.returncode == 0, result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)

    def get_file_permissions(self, filename):
        """Get current file permissions in octal"""
        try:
            stat_info = os.stat(filename)
            permissions = oct(stat_info.st_mode)[-3:]
            return permissions
        except Exception:
            return None

    def validate_chmod_command(self, user_command, expected_octal, filename):
        """Validate if chmod command produces correct permissions"""
        # Parse the command to understand what the user intended
        intended_mode, mode_type = self.parse_chmod_command(user_command, filename)
        
        if intended_mode is None:
            return False, f"Invalid command format: {mode_type}"
        
        # For octal mode, we can compare directly
        if mode_type == "octal":
            if intended_mode == expected_octal:
                return True, "Correct octal permissions"
            else:
                return False, f"Expected {expected_octal}, got {intended_mode}"
        
        # For symbolic mode, we need to execute and check the result
        elif mode_type == "symbolic":
            # Execute the command
            success, error = self.execute_chmod_safely(user_command, filename)
            if not success:
                return False, f"Command failed: {error}"
            
            # Check the resulting permissions
            actual_permissions = self.get_file_permissions(filename)
            if actual_permissions == expected_octal:
                return True, "Correct permissions set"
            else:
                # Convert back to symbolic for better error message
                expected_symbolic = self.octal_to_symbolic(expected_octal)
                actual_symbolic = self.octal_to_symbolic(actual_permissions) if actual_permissions else "unknown"
                return False, f"Expected {expected_symbolic}, got {actual_symbolic}"
        
        return False, "Unexpected error"

    def handle_client(self, conn, addr):
        """Handle individual client connection"""
        print(f"Handling connection from {addr}")
        
        try:
            # Generate random challenge
            perm_string, correct_octal = self.generate_random_permissions()
            
            # Create temporary file for this session
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
                temp_file.write("CTF Challenge File - Set correct permissions!\n")
                temp_filename = temp_file.name
            
            # Set initial safe permissions
            os.chmod(temp_filename, 0o600)
            
            welcome_msg = f"""
╔═══════════════════════════════════════════════════╗
║                  CHMOD CHALLENGE                  ║
╚═══════════════════════════════════════════════════╝

Set the permissions of the file to: {perm_string}

File: {temp_filename}

Allowed syntax examples:
• Octal: chmod 755 {temp_filename}
• Symbolic: chmod u=rwx,g=rx,o=r {temp_filename}  
• Relative: chmod g+w,o-r {temp_filename}

Your command: """
            
            conn.sendall(welcome_msg.encode())
            
            # Receive command
            data = conn.recv(1024).decode().strip()
            if not data:
                conn.sendall("\n❌ No command received.\n".encode())
                return
            
            # Validate command
            is_correct, message = self.validate_chmod_command(data, correct_octal, temp_filename)
            
            if is_correct:
                success_msg = f"""
✅ Correct! {message}

🎉 Congratulations! The flag is: {self.flag}

The correct permission {perm_string} corresponds to octal {correct_octal}
"""
                conn.sendall(success_msg.encode())
            else:
                error_msg = f"""
❌ Incorrect: {message}

💡 Hint: {perm_string} in octal is {correct_octal}
Try again with: chmod {correct_octal} {temp_filename}
"""
                conn.sendall(error_msg.encode())
                
        except Exception as e:
            conn.sendall(f"\n💥 Error: {str(e)}\n".encode())
        finally:
            # Cleanup
            try:
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
            except:
                pass
            conn.close()

    def start_server(self):
        """Start the challenge server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(10)
            print(f"🚀 CTF Challenge Server started on {self.host}:{self.port}")
            print("📝 Serving random chmod challenges...")
            print("⏹️  Server running in background mode")
            
            while True:
                conn, addr = server_socket.accept()
                # Handle each client in a separate thread
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n🛑 Server shutting down...")
        except Exception as e:
            print(f"💥 Server error: {e}")
        finally:
            server_socket.close()

if __name__ == "__main__":
    # Run server directly without terminal interaction
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--foreground":
        challenge = ChmodChallenge()
        challenge.start_server()
    else:
        # Run in background mode
        challenge = ChmodChallenge()
        challenge.start_server()