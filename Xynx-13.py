#!/usr/bin/env python3
"""
Xynx-13 Cipher Framework v1.23
ATPM License - Advanced Text Protection Module
Multi-layer encryption system with 16 standard encoding formats
"""

import os
import sys
import time
import base64
import binascii
import quopri
import urllib.parse
import hashlib
import json
import zlib
import ast
import codecs
from datetime import datetime

# ==================== CONFIGURATION SETTINGS ====================
class AppSettings:
    def __init__(self):
        self.typing_speed = 5
        self.animation_enabled = True
        self.color_enabled = True
        self.history_enabled = True
        self.auto_clear = True
        self.show_timestamp = True
        self.max_history = 50
        self.xynx_shift = 7
        self.xynx_xor_key = 0x2A

app_settings = AppSettings()

# ==================== TEXT ANIMATION FUNCTIONS ====================
def type_text(text, speed=None):
    """Print text with typing animation effect"""
    if speed is None:
        speed = 11 - app_settings.typing_speed
    
    if not app_settings.animation_enabled:
        print(text)
        return
    
    delay = 0.005 * speed
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def clear_screen():
    """Clear terminal screen (cross-platform)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_color(text, color_code=""):
    """Print colored text if enabled"""
    if app_settings.color_enabled and color_code:
        print(f"\033[{color_code}m{text}\033[0m")
    else:
        print(text)

# ==================== HEADER DISPLAY ====================
def print_header():
    """Display Xynx-13 ASCII logo and header"""
    header_logo = r"""
 __   __                      __ ____  
 \ \ / /                     /_ |___ \ 
  \ V /_   _ _ __ __  ________| | __) |
   > <| | | | '_ \\ \/ /______| ||__ < 
  / . \ |_| | | | |>  <       | |___) |
 /_/ \_\__, |_| |_/_/\_\      |_|____/ 
        __/ |                          
       |___/                            
"""
    print_color(header_logo, "36")
    print_color("Xynx-13 Cipher Framework v1.23 | ATPM License", "1;33")
    print_color("=" * 70, "34")
    if app_settings.show_timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print_color(f"Session started: {timestamp}", "90")

# ==================== XYnx-13 CORE CIPHER (12 LAYERS) ====================
def base36_encode(text):
    """Encode text to base36 (numbers + letters)"""
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num = int.from_bytes(text.encode(), 'big')
    if num == 0:
        return '0'
    result = ''
    while num > 0:
        num, rem = divmod(num, 36)
        result = alphabet[rem] + result
    return result

def base36_decode(text):
    """Decode base36 back to text"""
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num = 0
    for char in text:
        num = num * 36 + alphabet.index(char.upper())
    return num.to_bytes((num.bit_length() + 7) // 8, 'big').decode()

def base62_encode(text):
    """Encode text to base62 (numbers + upper/lowercase)"""
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    num = int.from_bytes(text.encode(), 'big')
    if num == 0:
        return '0'
    result = ''
    while num > 0:
        num, rem = divmod(num, 62)
        result = alphabet[rem] + result
    return result

def base62_decode(text):
    """Decode base62 back to text"""
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    num = 0
    for char in text:
        num = num * 62 + alphabet.index(char)
    return num.to_bytes((num.bit_length() + 7) // 8, 'big').decode()

def atbash_cipher(text):
    """Atbash cipher: A->Z, B->Y, etc."""
    result = ''
    for char in text:
        if 'a' <= char <= 'z':
            result += chr(219 - ord(char))
        elif 'A' <= char <= 'Z':
            result += chr(155 - ord(char))
        else:
            result += char
    return result

def rot47(text):
    """ROT47 cipher for all printable ASCII"""
    result = ''
    for char in text:
        if 33 <= ord(char) <= 126:
            result += chr(33 + ((ord(char) - 33 + 47) % 94))
        else:
            result += char
    return result

def rot47_reverse(text):
    """Reverse ROT47"""
    result = ''
    for char in text:
        if 33 <= ord(char) <= 126:
            result += chr(33 + ((ord(char) - 33 - 47) % 94))
        else:
            result += char
    return result

def xor_cipher(text, key=0x2A):
    """XOR cipher with fixed key"""
    result = ''
    for char in text:
        result += chr(ord(char) ^ key)
    return result

def ascii_shift(text, shift=3):
    """Shift ASCII values"""
    result = ''
    for char in text:
        if 32 <= ord(char) <= 126:
            new_ord = ord(char) + shift
            if new_ord > 126:
                new_ord = 32 + (new_ord - 127)
            elif new_ord < 32:
                new_ord = 127 - (32 - new_ord)
            result += chr(new_ord)
        else:
            result += char
    return result

def xynx13_encrypt(text):
    """12-layer Xynx-13 encryption"""
    if not text:
        return ""
    
    # Layer 1: Reverse
    result = text[::-1]
    # Layer 2: ROT13
    result = codecs.encode(result, 'rot13')
    # Layer 3: Atbash
    result = atbash_cipher(result)
    # Layer 4: ROT47
    result = rot47(result)
    # Layer 5: Base36
    result = base36_encode(result)
    # Layer 6: XOR
    result = xor_cipher(result, app_settings.xynx_xor_key)
    # Layer 7: ASCII Shift (+3)
    result = ascii_shift(result, 3)
    # Layer 8: Base62
    result = base62_encode(result)
    # Layer 9: ROT13 again
    result = codecs.encode(result, 'rot13')
    # Layer 10: Reverse again
    result = result[::-1]
    # Layer 11: Caesar (shift from settings)
    result = ascii_shift(result, app_settings.xynx_shift)
    # Layer 12: Base36 final compression
    result = base36_encode(result)
    
    return result

def xynx13_decrypt(text):
    """12-layer Xynx-13 decryption (reverse order)"""
    if not text:
        return ""
    
    # Layer 12 reverse: Base36 decode
    result = base36_decode(text)
    # Layer 11 reverse: Reverse ASCII shift
    result = ascii_shift(result, -app_settings.xynx_shift)
    # Layer 10 reverse: Reverse text
    result = result[::-1]
    # Layer 9 reverse: ROT13
    result = codecs.decode(result, 'rot13')
    # Layer 8 reverse: Base62 decode
    result = base62_decode(result)
    # Layer 7 reverse: Reverse ASCII shift
    result = ascii_shift(result, -3)
    # Layer 6 reverse: XOR (same key)
    result = xor_cipher(result, app_settings.xynx_xor_key)
    # Layer 5 reverse: Base36 decode
    result = base36_decode(result)
    # Layer 4 reverse: Reverse ROT47
    result = rot47_reverse(result)
    # Layer 3 reverse: Atbash (same function)
    result = atbash_cipher(result)
    # Layer 2 reverse: ROT13
    result = codecs.decode(result, 'rot13')
    # Layer 1 reverse: Reverse text
    result = result[::-1]
    
    return result

# ==================== OPERATION HISTORY ====================
operation_history = []

def add_to_history(operation, input_text, result):
    """Add operation to history"""
    if app_settings.history_enabled and len(operation_history) < app_settings.max_history:
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = {
            'time': timestamp,
            'operation': operation,
            'input': input_text[:50] + '...' if len(input_text) > 50 else input_text,
            'result': result[:50] + '...' if len(result) > 50 else result
        }
        operation_history.append(entry)

def show_history():
    """Display operation history"""
    if not operation_history:
        type_text("No operations recorded in history.", 5)
        return
    
    print_color("\n" + "=" * 70, "35")
    print_color("OPERATION HISTORY", "1;35")
    print_color("=" * 70, "35")
    
    for i, entry in enumerate(reversed(operation_history[-10:]), 1):
        print_color(f"[{entry['time']}] {entry['operation']}", "90")
        print_color(f"  Input: {entry['input']}", "37")
        print_color(f"  Output: {entry['result']}", "36")
        if i < len(operation_history[-10:]):
            print_color("-" * 60, "90")
    
    print_color("=" * 70, "35")

# ==================== STANDARD ENCODING OPERATIONS ====================
def get_input_text(prompt):
    """Get user input with back/exit options"""
    print_color(f"\n{prompt}", "1;33")
    print_color("Type 'BACK' to return to menu or 'EXIT' to quit: ", "90")
    text = input()
    if text.upper() == 'BACK':
        return None
    elif text.upper() == 'EXIT':
        type_text("Thank you for using Xynx-13. Goodbye!", 5)
        sys.exit(0)
    return text

def print_result_box(result):
    """Display result in formatted box"""
    print_color("\n" + "=" * 70, "32")
    print_color("RESULT:", "1;32")
    print_color("=" * 70, "32")
    print_color(result, "1;37")
    print_color("=" * 70, "32")

def base64_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        if mode == 'encode':
            result = base64.b64encode(text.encode()).decode()
            op_name = "Base64 Encode"
        else:
            result = base64.b64decode(text.encode()).decode()
            op_name = "Base64 Decode"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def url_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        if mode == 'encode':
            result = urllib.parse.quote(text)
            op_name = "URL Encode"
        else:
            result = urllib.parse.unquote(text)
            op_name = "URL Decode"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def hex_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        if mode == 'encode':
            result = binascii.hexlify(text.encode()).decode()
            op_name = "Hex Encode"
        else:
            result = binascii.unhexlify(text.encode()).decode()
            op_name = "Hex Decode"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def binary_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        if mode == 'encode':
            result = ' '.join(format(ord(c), '08b') for c in text)
            op_name = "Binary Encode"
        else:
            text = text.replace(' ', '')
            binary_values = [text[i:i+8] for i in range(0, len(text), 8)]
            result = ''.join([chr(int(b, 2)) for b in binary_values])
            op_name = "Binary Decode"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def quoted_printable_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        if mode == 'encode':
            result = quopri.encodestring(text.encode()).decode()
            op_name = "QP Encode"
        else:
            result = quopri.decodestring(text.encode()).decode()
            op_name = "QP Decode"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def rot13_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        result = codecs.encode(text, 'rot13')
        op_name = "ROT13"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def caesar_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        shift = int(input("Enter shift value (1-25): "))
        if not 1 <= shift <= 25:
            print_color("Shift must be 1-25", "91")
            return
        result = ''
        for char in text:
            if 'a' <= char <= 'z':
                if mode == 'encode':
                    result += chr((ord(char) - 97 + shift) % 26 + 97)
                else:
                    result += chr((ord(char) - 97 - shift) % 26 + 97)
            elif 'A' <= char <= 'Z':
                if mode == 'encode':
                    result += chr((ord(char) - 65 + shift) % 26 + 65)
                else:
                    result += chr((ord(char) - 65 - shift) % 26 + 65)
            else:
                result += char
        op_name = f"Caesar {mode} (shift {shift})"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except ValueError:
        print_color("Invalid shift value", "91")

def xor_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        key = input("Enter XOR key (any character): ")
        if not key:
            print_color("Key cannot be empty", "91")
            return
        key_char = key[0]
        result = ''
        for char in text:
            result += chr(ord(char) ^ ord(key_char))
        if mode == 'encode':
            result = binascii.hexlify(result.encode()).decode()
        op_name = f"XOR {mode}"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def md5_operation():
    text = get_input_text("Enter text to hash:")
    if text is None: return
    try:
        result = hashlib.md5(text.encode()).hexdigest()
        op_name = "MD5 Hash"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def sha256_operation():
    text = get_input_text("Enter text to hash:")
    if text is None: return
    try:
        result = hashlib.sha256(text.encode()).hexdigest()
        op_name = "SHA-256 Hash"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def json_operation(mode):
    text = get_input_text("Enter JSON text:")
    if text is None: return
    try:
        if mode == 'encode':
            obj = json.loads(text)
            result = json.dumps(obj, indent=2)
            op_name = "JSON Encode"
        else:
            try:
                obj = json.loads(text)
                result = json.dumps(obj, indent=2)
            except:
                result = str(ast.literal_eval(text))
            op_name = "JSON Decode"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def zlib_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        if mode == 'encode':
            result = base64.b64encode(zlib.compress(text.encode())).decode()
            op_name = "Zlib Compress"
        else:
            result = zlib.decompress(base64.b64decode(text.encode())).decode()
            op_name = "Zlib Decompress"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def morse_operation(mode):
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
        ' ': '/'
    }
    reverse_morse = {v: k for k, v in morse_dict.items()}
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        if mode == 'encode':
            result = ' '.join(morse_dict.get(c.upper(), '') for c in text)
            op_name = "Morse Encode"
        else:
            words = text.split(' / ')
            result = ''
            for word in words:
                chars = word.split()
                result += ''.join(reverse_morse.get(c, '') for c in chars)
                result += ' '
            result = result.strip()
            op_name = "Morse Decode"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def reverse_operation():
    text = get_input_text("Enter text to reverse:")
    if text is None: return
    try:
        result = text[::-1]
        op_name = "Reverse Text"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def ascii_code_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        if mode == 'encode':
            result = ' '.join(str(ord(c)) for c in text)
            op_name = "ASCII Encode"
        else:
            codes = text.split()
            result = ''.join(chr(int(code)) for code in codes)
            op_name = "ASCII Decode"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

def utf8_operation(mode):
    text = get_input_text("Enter text to process:")
    if text is None: return
    try:
        if mode == 'encode':
            result = text.encode('utf-8').hex()
            op_name = "UTF-8 Encode"
        else:
            result = bytes.fromhex(text).decode('utf-8')
            op_name = "UTF-8 Decode"
        print_result_box(result)
        add_to_history(op_name, text, result)
    except Exception as e:
        print_color(f"Error: {e}", "91")

# ==================== SINGLE PHRASE MENU ====================
def single_phrase_menu():
    """Handle single phrase encoding/decoding operations"""
    while True:
        clear_screen()
        print_header()
        print_color("\n" + "=" * 70, "36")
        print_color("SINGLE PHRASE ENCODE/DECODE - Select Language:", "1;36")
        print_color("=" * 70, "36")
        
        languages = [
            ("1", "Base64"),
            ("2", "URL"),
            ("3", "Hexadecimal"),
            ("4", "Binary"),
            ("5", "Quoted-Printable"),
            ("6", "ROT13"),
            ("7", "Caesar Cipher"),
            ("8", "XOR"),
            ("9", "MD5 Hash (encode only)"),
            ("10", "SHA-256 Hash (encode only)"),
            ("11", "JSON"),
            ("12", "Zlib Compression"),
            ("13", "Morse Code"),
            ("14", "Reverse Text"),
            ("15", "ASCII Code"),
            ("16", "UTF-8"),
            ("17", "Back to Main Menu")
        ]
        
        for num, lang in languages:
            color = "32" if num in ["9", "10"] else "36"
            print_color(f"[{num}] {lang}", color)
        
        print_color("=" * 70, "36")
        
        choice = input("\nSelect language [1-17]: ").strip()
        
        if choice == '17':
            break
            
        if choice not in [str(i) for i in range(1, 17)]:
            type_text("Invalid selection.", 5)
            continue
        
        # Get encode/decode mode (except for hashes)
        if choice in ['9', '10']:
            mode = 'encode'
        else:
            print_color("\nEncode or Decode? (E/D): ", "1;33")
            mode_input = input().lower()
            if mode_input in ['e', 'encode']:
                mode = 'encode'
            elif mode_input in ['d', 'decode']:
                mode = 'decode'
            else:
                type_text("Invalid selection.", 5)
                continue
        
        # Execute selected operation
        operations = {
            '1': lambda m: base64_operation(m),
            '2': lambda m: url_operation(m),
            '3': lambda m: hex_operation(m),
            '4': lambda m: binary_operation(m),
            '5': lambda m: quoted_printable_operation(m),
            '6': lambda m: rot13_operation(m),
            '7': lambda m: caesar_operation(m),
            '8': lambda m: xor_operation(m),
            '9': lambda m: md5_operation(),
            '10': lambda m: sha256_operation(),
            '11': lambda m: json_operation(m),
            '12': lambda m: zlib_operation(m),
            '13': lambda m: morse_operation(m),
            '14': lambda m: reverse_operation(),
            '15': lambda m: ascii_code_operation(m),
            '16': lambda m: utf8_operation(m)
        }
        
        if choice in operations:
            operations[choice](mode)
            print_color("\nPress Enter to continue...", "90")
            input()

# ==================== XYnx-13 OPERATION ====================
def xynx13_operation():
    """Handle Xynx-13 encryption/decryption"""
    clear_screen()
    print_header()
    
    print_color("\n" + "=" * 70, "35")
    print_color("XYNX-13 12-LAYER CIPHER", "1;35")
    print_color("=" * 70, "35")
    print_color("Proprietary multi-layer encryption system", "90")
    print_color("=" * 70, "35")
    
    while True:
        print_color("\nEncrypt or Decrypt? (E/D) or 'BACK' for main menu: ", "1;33")
        mode = input().lower()
        
        if mode == 'back':
            break
            
        if mode not in ['e', 'd', 'encrypt', 'decrypt']:
            type_text("Invalid selection. Use E, D, or BACK", 5)
            continue
        
        text = get_input_text("Enter text to process:")
        if text is None:
            continue
        
        try:
            if mode in ['e', 'encrypt']:
                result = xynx13_encrypt(text)
                op_name = "Xynx-13 Encrypt"
            else:
                result = xynx13_decrypt(text)
                op_name = "Xynx-13 Decrypt"
            
            print_result_box(result)
            add_to_history(op_name, text, result)
            
            print_color("\nPress Enter to continue...", "90")
            input()
            
        except Exception as e:
            print_color(f"Error: {e}", "91")
            print_color("\nPress Enter to continue...", "90")
            input()

# ==================== SETTINGS MENU ====================
def settings_menu():
    """Handle application settings"""
    global app_settings
    
    while True:
        clear_screen()
        print_header()
        
        print_color("\n" + "=" * 70, "33")
        print_color("APPLICATION SETTINGS", "1;33")
        print_color("=" * 70, "33")
        
        settings_list = [
            ("1", f"Typing Speed: [{app_settings.typing_speed}/10]", "36"),
            ("2", f"Animations: {'ENABLED' if app_settings.animation_enabled else 'DISABLED'}", "36"),
            ("3", f"Colors: {'ENABLED' if app_settings.color_enabled else 'DISABLED'}", "36"),
            ("4", f"History: {'ENABLED' if app_settings.history_enabled else 'DISABLED'}", "32"),
            ("5", f"Auto Clear: {'ENABLED' if app_settings.auto_clear else 'DISABLED'}", "32"),
            ("6", f"Timestamp: {'SHOWN' if app_settings.show_timestamp else 'HIDDEN'}", "32"),
            ("7", f"Xynx-13 Caesar Shift: [{app_settings.xynx_shift}]", "35"),
            ("8", f"Xynx-13 XOR Key: [0x{app_settings.xynx_xor_key:02X}]", "35"),
            ("9", "Restore Default Settings", "33"),
            ("10", "Back to Main Menu", "90")
        ]
        
        for num, text, color in settings_list:
            print_color(f"[{num}] {text}", color)
        
        print_color("=" * 70, "33")
        
        choice = input("\nSelect setting to change [1-10]: ").strip()
        
        if choice == '1':
            try:
                speed = int(input("Enter typing speed (1-10, 10=fastest): "))
                if 1 <= speed <= 10:
                    app_settings.typing_speed = speed
                    type_text(f"Typing speed set to {speed}/10", 5)
                else:
                    type_text("Please enter 1-10", 5)
            except ValueError:
                type_text("Invalid input", 5)
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            app_settings.animation_enabled = not app_settings.animation_enabled
            status = "ENABLED" if app_settings.animation_enabled else "DISABLED"
            type_text(f"Animations {status}", 5)
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            app_settings.color_enabled = not app_settings.color_enabled
            status = "ENABLED" if app_settings.color_enabled else "DISABLED"
            type_text(f"Colors {status}", 5)
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            app_settings.history_enabled = not app_settings.history_enabled
            status = "ENABLED" if app_settings.history_enabled else "DISABLED"
            type_text(f"History {status}", 5)
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            app_settings.auto_clear = not app_settings.auto_clear
            status = "ENABLED" if app_settings.auto_clear else "DISABLED"
            type_text(f"Auto Clear {status}", 5)
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            app_settings.show_timestamp = not app_settings.show_timestamp
            status = "SHOWN" if app_settings.show_timestamp else "HIDDEN"
            type_text(f"Timestamp {status}", 5)
            input("\nPress Enter to continue...")
        
        elif choice == '7':
            try:
                shift = int(input("Enter Xynx-13 Caesar shift value (1-25): "))
                if 1 <= shift <= 25:
                    app_settings.xynx_shift = shift
                    type_text(f"Xynx-13 shift set to {shift}", 5)
                else:
                    type_text("Please enter 1-25", 5)
            except ValueError:
                type_text("Invalid input", 5)
            input("\nPress Enter to continue...")
        
        elif choice == '8':
            try:
                key = input("Enter Xynx-13 XOR key (0-255, hex like 0x2A or decimal): ")
                if key.startswith('0x'):
                    xor_key = int(key, 16)
                else:
                    xor_key = int(key)
                if 0 <= xor_key <= 255:
                    app_settings.xynx_xor_key = xor_key
                    type_text(f"XOR key set to 0x{xor_key:02X}", 5)
                else:
                    type_text("Please enter 0-255", 5)
            except ValueError:
                type_text("Invalid input", 5)
            input("\nPress Enter to continue...")
        
        elif choice == '9':
            new_settings = AppSettings()
            app_settings.typing_speed = new_settings.typing_speed
            app_settings.animation_enabled = new_settings.animation_enabled
            app_settings.color_enabled = new_settings.color_enabled
            app_settings.history_enabled = new_settings.history_enabled
            app_settings.auto_clear = new_settings.auto_clear
            app_settings.show_timestamp = new_settings.show_timestamp
            app_settings.xynx_shift = new_settings.xynx_shift
            app_settings.xynx_xor_key = new_settings.xynx_xor_key
            type_text("Default settings restored", 5)
            input("\nPress Enter to continue...")
        
        elif choice == '10':
            break
        else:
            type_text("Invalid selection.", 5)
            input("\nPress Enter to continue...")

# ==================== MAIN APPLICATION LOOP ====================
def main():
    """Main application entry point"""
    try:
        type_text("Initializing Xynx-13 Cipher Framework...", 7)
        time.sleep(0.5)
        type_text("Loading 12-layer encryption engine...", 7)
        time.sleep(0.3)
        type_text("System ready.", 7)
        time.sleep(0.7)
        
        while True:
            if app_settings.auto_clear:
                clear_screen()
            
            print_header()
            
            print_color("\n" + "=" * 70, "34")
            print_color("MAIN MENU:", "1;34")
            print_color("=" * 70, "34")
            print_color("[1] Xynx-13 Encode/Decode (12-Layer Cipher)", "36")
            print_color("[2] Single Phrase Encode/Decode (16 Languages)", "36")
            print_color("[3] Operation Logs", "35")
            print_color("[4] Settings", "33")
            print_color("[5] Exit Session", "31")
            print_color("=" * 70, "34")
            
            choice = input("\nEnter your choice [1-5]: ").strip()
            
            if choice == '1':
                xynx13_operation()
            
            elif choice == '2':
                single_phrase_menu()
            
            elif choice == '3':
                clear_screen()
                print_header()
                show_history()
                input("\nPress Enter to continue...")
            
            elif choice == '4':
                settings_menu()
            
            elif choice == '5':
                type_text("\nThank you for using Xynx-13. Goodbye!", 5)
                time.sleep(1)
                break
            
            else:
                type_text("Invalid selection. Please enter 1-5.", 5)
                time.sleep(1)
    
    except KeyboardInterrupt:
        print_color("\n\nSession terminated by user.", "33")
        type_text("Thank you for using Xynx-13. Goodbye!", 5)
    except Exception as e:
        print_color(f"\nUnexpected error: {e}", "91")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()