import sys
import time
import os
import pyperclip  # Requires: pip install pyperclip

def banner():
    print("""
   ___ __ _  ___ ___  __ _ _ __ 
  / __/ _` |/ _ \/ __|/ _` | '__|
 | (_| (_| |  __/\__ \ (_| | |   
  \___\__,_|\___||___/\__,_|_|   
    CAESAR CIPHER CLI V1.2 (File + Clipboard)
    """)

def process_text(text, shift, mode='encrypt'):
    result = ""
    if mode == 'decrypt':
        shift = -shift

    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            processed_char = chr((ord(char) - start + shift) % 26 + start)
            result += processed_char
        else:
            result += char
    return result

def brute_force_crack(text):
    print("\n[!] ATTEMPTING TO CRACK MESSAGE...\n")
    time.sleep(1)
    # Try all 25 possible shifts
    for possible_shift in range(1, 26):
        attempt = process_text(text, possible_shift, mode='decrypt')
        print(f"Key #{possible_shift}: {attempt}")
        time.sleep(0.05)
    print("\n[+] Scanning complete. Scroll up to find the readable sentence.")

def handle_file_process(mode):
    """Handles reading from a file and writing to a new one."""
    filename = input(f"\n[?] Enter the filename to {mode} (e.g., secret.txt): ")
    
    if not os.path.exists(filename):
        print(f"\n[!] Error: File '{filename}' not found.")
        return

    try:
        key = int(input("Enter shift key (1-25): "))
        
        print(f"Reading '{filename}'...")
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = process_text(content, key, mode)
        
        output_filename = f"{mode}ed_{filename}"
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(result)
            
        print(f"\n[SUCCESS] Content {mode}ed!")
        print(f"[SAVED] Saved to new file: {output_filename}")
        
    except ValueError:
        print("\n[!] Error: Key must be a number.")
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")

def main():
    while True:
        banner()
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Crack a message (Brute Force)")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ")

        if choice == '1' or choice == '2':
            mode = 'encrypt' if choice == '1' else 'decrypt'
            method = input(f"\nType 'T' to {mode} Text, or 'F' to {mode} a File: ").upper()
            
            if method == 'F':
                handle_file_process(mode)
            elif method == 'T':
                msg = input(f"Enter message to {mode}: ")
                try:
                    key = int(input("Enter shift key (1-25): "))
                    result = process_text(msg, key, mode)
                    print(f"\n[RESULT]: {result}")
                    
                    # --- CLIPBOARD INTEGRATION ---
                    pyperclip.copy(result)
                    print("[✓] Copied to clipboard automatically!")
                    
                except ValueError:
                    print("\n[!] Error: Key must be a number.")
            else:
                print("\n[!] Invalid option.")
            
            input("\nPress Enter to continue...")

        elif choice == '3':
            msg = input("Enter the encrypted message: ")
            brute_force_crack(msg)
            input("\nPress Enter to continue...")

        elif choice == '4':
            print("Exiting...")
            sys.exit()
        
        else:
            print("Invalid selection.")
            time.sleep(1)

if __name__ == "__main__":
    main()