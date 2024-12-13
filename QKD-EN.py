import os
import random 
import logging  
import hashlib  
import math  
import time  
from datetime import datetime  
from typing import List, Tuple, Optional  

if os.name == 'nt': # For Windows  
    os.system('title Quantum Key Distribution')  
else: # For Unix/Linux/Mac  
    print("\033]0;Quantum Key Distribution\007")  

# Constants  
PREVIEW_LINE_LENGTH = 50  
PROGRESS_BAR_LENGTH = 30  

# Setup logging  
logging.basicConfig(  
    level=logging.WARNING,  
    format='%(asctime)s - %(levelname)s: %(message)s',  
    datefmt='%Y-%m-%d %H:%M:%S'  
)  

def show_progress(current: int, total: int, prefix: str = '', suffix: str = ''):  
    """Show progress bar with percentage"""  
    filled = int(round(PROGRESS_BAR_LENGTH * current / float(total)))  
    bar = '=' * filled + '-' * (PROGRESS_BAR_LENGTH - filled)  
    percent = round(100.0 * current / float(total), 1)  
    print(f'\r{prefix} [{bar}] {percent}% {suffix}', end='\r')  
    if current == total:  
        print()  

class SecureBB84:  
    """Implementation of BB84 protocol for Quantum Key Distribution"""  
    def __init__(self):  
        self.bases = ['rectilinear', 'diagonal']  
        self.error_threshold = 0.15  
        self.num_qubits = 1000000  
        self.min_key_length = 500  
        self.verification_bits = 40  
        self.noise_threshold = 0.95  
        self.chunk_size = 1000  

    def secure_random(self) -> int:  
        """Generate safe random bits"""  
        return random.getrandbits(1)  

    def simulate_transmission(self, bit: int, send_basis: str, receive_basis: str) -> Tuple[int, float]:  
        """Qubit transmission simulation"""  
        if send_basis == receive_basis:  
            return bit, 1.0  
        return self. secure_random(), 0.5  

    def verify_key_security(self, key: List[int]) -> bool:  
        """Key security verification"""  
        if len(key) < self.min_key_length:  
            return False  
        ones = sum(key) / len(key)  
        return 0.3 <= ones <= 0.7  

    def generate_key(self) -> Tuple[Optional[List[int]], float]:  
        """Generate new quantum key"""  
        try:  
            retry_count = 0  
            max_retries = 3  
            
            while retry_count < max_retries:  
                # Generate quantum bits  
                alice_bits = [self.secure_random() for _ in range(self.num_qubits)]  
                alice_bases = [random.choice(self.bases) for _ in range(self.num_qubits)]  
                bob_bases = [random.choice(self.bases) for _ in range(self.num_qubits)]  
                
                received_bits = []  
                received_confidence = []  
                
                # Simulate transmission with progress  
                for i in range(self.num_qubits):  
                    bit, conf = self.simulate_transmission(  
                        alice_bits[i],  
                        alice_bases[i],  
                        bob_bases[i]  
                    )  
                    received_bits.append(bit)  
                    received_confidence.append(conf)  
                    
                    if i % 100 == 0:  
                        show_progress(i, self.num_qubits, 'Generating quantum key: ')  
                
                show_progress(self.num_qubits, self.num_qubits, 'Generating quantum key: ')  
                
                # Key sifting  
                sifted_key = []  
                verification_bits = []  
                errors = 0  
                total_matched = 0  
                
                print("\nSifting quantum key...")  
                for i in range(self.num_qubits):  
                    if alice_bases[i] == bob_bases[i]:  
                        total_matched += 1  
                        if alice_bits[i] != received_bits[i]:  
                            errors += 1  
                        
                        if len(verification_bits) < self.verification_bits:  
                            verification_bits.append(alice_bits[i])  
                        else:  
                            sifted_key.append(alice_bits[i])  
                    
                    if i % 100 == 0:  
                        show_progress(i, self.num_qubits, 'Shifting key: ')  
                        
                show_progress(self.num_qubits, self.num_qubits, 'Shifting key: ')  
                
                if total_matched == 0:  
                    retry_count += 1  
                    continue  
                    
                error_rate = errors / total_matched  
                
                if len(sifted_key) >= self.min_key_length and error_rate <= self.error_threshold:  
                    return sifted_key, error_rate  
                    
                retry_count += 1  
                print(f"\nRetry {retry_count}/{max_retries} - Error rate too high")  
                
            return None, 1.0  
            
        except Exception as e:  
            logging.error(f"Key generation error: {str(e)}")  
            return None, 1.0  

class EnhancedQKDSimulator:  
    """Enhanced Quantum Key Distribution Simulator with additional features"""  
    def __init__(self):  
        self.bb84 = SecureBB84()  
        self.current_key = None  
        self.key_hash = None  
        self.use_count = 0  
        self.chunk_size = self.bb84.chunk_size  
        self.key_pool = []  

    def text_to_binary(self, text: str) -> str:  
        """Convert text to binary with newline preservation"""  
        try:  
            lines = []  
            for line in text.split('\n'):  
                lines.append(' '.join(line.split()))  
            normalized_text = '\n'.join(lines)  
            
            text_bytes = normalized_text.encode('utf-8')  
            binary_chunks = []  
            for byte in text_bytes:  
                binary_chunks.append(format(byte, '08b'))  
            message_bits = ''.join(binary_chunks)  
            length_bits = format(len(message_bits), '032b')  
            return length_bits + message_bits  
        except Exception as e:  
            logging.error(f"Text to binary error: {str(e)}")  
            return None  

    def binary_to_text(self, binary: str) -> str:  
        """Binary to text conversion with newline preservation"""  
        try:  
            message_length = int(binary[:32], 2)  
            message_bits = binary[32:32+message_length]  
            
            if len(message_bits) % 8 != 0:  
                padding = 8 - (len(message_bits) % 8)  
                message_bits += '0' * padding  
            
            byte_chunks = [message_bits[i:i+8] for i in range(0, len(message_bits), 8)]  
            bytes_data = bytearray()  
            
            for chunk in byte_chunks:  
                if len(chunk) == 8:  
                    try:  
                        byte_val = int(chunk, 2)  
                        if byte_val < 256:  
                            bytes_data.append(byte_val)  
                    except ValueError:  
                        continue  
            
            try:  
                decoded = bytes_data.decode('utf-8', errors='ignore')  
                lines = []  
                for line in decoded.split('\n'):  
                    lines.append(' '.join(line.split()))  
                return '\n'.join(lines)  
            except UnicodeDecodeError:  
                return bytes_data.decode('latin-1', errors='ignore')  
                
        except Exception as e:  
            logging.error(f"Binary to text error: {str(e)}")  
            return None  

    def generate_key_pool(self, needed_length: int) -> bool:  
        """Generate quantum key pool as needed"""  
        try:  
            current_length = sum(len(k) for k in self.key_pool)  
            while current_length < needed_length:  
                print(f"\nGenerating additional keys ({current_length}/{needed_length} bits available)")  
                key, error_rate = self.bb84.generate_key()  
                if not key:  
                    return False  
                self.key_pool.append(key)  
                current_length += len(key)  
                show_progress(current_length, needed_length, 'Key pool: ')  
            return True  
        except Exception as e:  
            logging.error(f"Key pool generation error: {str(e)}")  
            return False  

    def get_key_from_pool(self, length: int) -> List[int]:  
        """Take the key from the pool according to the required length"""  
        result = []  
        while len(result) < length:  
            if not self.key_pool:  
                if not self.generate_key_pool(length - len(result)):  
                    raise Exception("Failed to generate enough keys")  
            current_key = self.key_pool[0]  
            needed = length - len(result)  
            if len(current_key) <= needed:  
                result.extend(current_key)  
                self.key_pool.pop(0)  
            else:  
                result.extend(current_key[:needed])  
                self.key_pool[0] = current_key[needed:]  
        return result  

    def get_multiline_input(self) -> str:  
        """Multiline input with 4 enter limit"""  
        enter_count = 0  
        message_lines = []  
        
        print("\nEnter message (maximum 4 consecutive enters):")  
        print("Type 'CANCEL' on a new line to cancel")  
        print("-" * PREVIEW_LINE_LENGTH)  
        
        while enter_count < 4:  
            try:  
                line = input()  
                
                if line.upper() == 'CANCEL':  
                    return None  
                    
                message_lines.append(line)  
                
                if line.strip() == '':  
                    enter_count += 1  
                else:  
                    enter_count = 0  
                    
            except KeyboardInterrupt:  
                print("\nInput canceled!")  
                return None  
                
        return '\n'.join(message_lines)  

    def encrypt_and_share(self, message: str = '') -> Tuple[Optional[str], Optional[str]]:  
        """Encrypt and prepare message for sharing"""  
        try:  
            if not message:  
                message = self.get_multiline_input()  
                
            if not message or message.isspace():  
                print("\nMessage cannot be empty!")  
                return None, None  

            print("\nMessage to be encrypted:")  
            print("-" * PREVIEW_LINE_LENGTH)  
            lines = message.split('\n')  
            if len(lines) > 5:  
                for line in lines[:5]:  
                    print(line)  
                print(f"\n... {len(lines) - 5} more lines ...")  
            else:  
                for line in lines:  
                    print(line)  
            print("-" * PREVIEW_LINE_LENGTH)  
            print(f"Total lines: {len(lines)}")  
            print(f"Total characters: {len(message)}")  
            
            if input("\nContinue encryption? (y/n): ").lower() != 'y':  
                return None, None  

            # Split message into chunks  
            message_chunks = [  
                message[i:i+self.chunk_size]   
                for i in range(0, len(message), self.chunk_size)  
            ]  

            total_chunks = len(message_chunks)  
            print(f"\nProcessing {total_chunks} chunks...")  

            encrypted_chunks = []  
            keys_used = []  

            # Encrypt each chunk  
            for i, chunk in enumerate(message_chunks, 1):  
                print(f"\nProcessing chunk {i}/{total_chunks}")  
                binary_chunk = self.text_to_binary(chunk)  
                if not binary_chunk:  
                    return None, None  

                chunk_length = len(binary_chunk)  
                
                try:  
                    chunk_key = self.get_key_from_pool(chunk_length)  
                except Exception as e:  
                    print("\nFailed to generate quantum key")  
                    return None, None  

                encrypted_bits = [  
                    str(int(a) ^ b)  
                    for a, b in zip(binary_chunk, chunk_key)  
                ]  
                encrypted_chunks.append(''.join(encrypted_bits))  
                keys_used.append(chunk_key)  
                
                show_progress(i, total_chunks, 'Encryption: ')  

            print("\nCreating transport key...")  
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  
            salt = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()[:16]  
            transport_key = hashlib.pbkdf2_hmac(  
                'sha256',  
                salt.encode(),  
                timestamp.encode(),  
                100000  
            ).hex()[:32]  

            print("Encrypting key...")  
            all_keys = []  
            for i, key in enumerate(keys_used, 1):  
                key_str = ','.join(map(str, key))  
                key_bytes = key_str.encode()  
                encrypted_key = [  
                    kb ^ int(transport_key[i % len(transport_key)], 16)  
                    for i, kb in enumerate(key_bytes)  
                ]  
                all_keys.append(''.join(map(lambda x: format(x, '02x'), encrypted_key)))  
                show_progress(i, len(keys_used), 'Key encryption: ')  

            print("\nPreparing export data...")  
            encrypted_str = '###'.join(all_keys)  
            encrypted_message = '###'.join(encrypted_chunks)  
            
            ver_hash = hashlib.sha256(  
                f"{timestamp}{salt}{encrypted_str}{encrypted_message}".encode()  
            ).hexdigest()  

            filename = f"qkd_message_{timestamp}.qk"  
            export_str = "@@@".join([  
                timestamp,  
                salt,  
                encrypted_str,  
                encrypted_message,  
                ver_hash,  
                str(total_chunks)  
            ])  
            
            print("Saving file...")  
            with open(filename, 'w', encoding='utf-8') as f:  
                f.write(export_str)  

            recovery_code = hashlib.sha256(transport_key.encode()).hexdigest()[:12]  

            return filename, recovery_code  

        except Exception as e:  
            logging.error(f"Encryption error: {str(e)}")  
            return None, None  

    def decrypt_shared_message(self, filename: str, recovery_code: str) -> Optional[str]:  
        """Decrypt encrypted messages"""  
        try:  
            print("\nReading file...")  
            with open(filename, 'r', encoding='utf-8') as f:  
                data = f.read().strip()  

            parts = data.split("@@@")  
            if len(parts) != 6:  
                print("\nInvalid file format")  
                return None  

            timestamp, salt, encrypted_keys_str, encrypted_message, ver_hash, chunk_count = parts  
            chunk_count = int(chunk_count)  

            print("Verifying file integrity...")  
            check_hash = hashlib.sha256(  
                f"{timestamp}{salt}{encrypted_keys_str}{encrypted_message}".encode()  
            ).hexdigest()  

            if check_hash != ver_hash:  
                print("\nWarning: File has been modified!")  
                if input("Continue decryption? (y/n): ").lower() != 'y':  
                    return None  

            print("Creating transport key...")
            transport_key = hashlib.pbkdf2_hmac(  
                'sha256',  
                salt.encode(),  
                timestamp.encode(),  
                100000  
            ).hex()[:32]  

            print("Verify recovery code...")  
            check_code = hashlib.sha256(transport_key.encode()).hexdigest()[:12]  
            if check_code != recovery_code:  
                print("\nRecovery code is invalid!")  
                return None  

            encrypted_keys = encrypted_keys_str.split("###")  
            encrypted_chunks = encrypted_message.split("###")  

            if len(encrypted_keys) != chunk_count or len(encrypted_chunks) != chunk_count:  
                print("\nData chunks are invalid")  
                return None  

            print(f"\nProcessing {chunk_count} chunks...")  
            decrypted_chunks = []  
            
            for i in range(chunk_count):  
                try:  
                    # Decrypt key  
                    encrypted_key_bytes = bytes.fromhex(encrypted_keys[i])  
                    decrypted_key = []  
                    for j, eb in enumerate(encrypted_key_bytes):  
                        tk_byte = int(transport_key[j % len(transport_key)], 16)  
                        decrypted_key.append(eb ^ tk_byte)  
                    key_str = bytes(decrypted_key).decode('utf-8', errors='ignore')  
                    chunk_key = [int(k) for k in key_str.split(',') if k.strip()]  

                    # Decrypt message chunk  
                    decrypted_bits = [  
                        str(int(a) ^ b)  
                        for a, b in zip(encrypted_chunks[i], chunk_key)  
                    ]  
                    decrypted_binary = ''.join(decrypted_bits)  
                    decrypted_chunk = self.binary_to_text(decrypted_binary)  
                    
                    if decrypted_chunk:  
                        decrypted_chunks.append(decrypted_chunk)  
                    else:  
                        raise Exception(f"Failed to decrypt chunk {i+1}")  
                        
                    show_progress(i+1, chunk_count, 'Description: ')  

                except Exception as e:  
                    logging.error(f"Chunk {i+1} decryption error: {str(e)}")  
                    return None  

            decrypted_text = ''.join(decrypted_chunks)  
            
            # Format output with correct line breaks  
            formatted_lines = decrypted_text.split('\n')  

            print("\n=== Decrypted Message ===")  
            print("-" * PREVIEW_LINE_LENGTH)  
            
            # Preview first 5 lines  
            preview_lines = formatted_lines[:5]  
            for line in preview_lines:  
                print(line)  
                
            if len(formatted_lines) > 5:  
                print(f"\n... {len(formatted_lines) - 5} more lines ...")  
            
            print("-" * PREVIEW_LINE_LENGTH)  
            print(f"Total lines: {len(formatted_lines)}")  
            print(f"Total characters: {len(decrypted_text)}")  

            # Display and storage options  
            while True:  
                print("\nOptions:")  
                print("1. Display all messages")  
                print("2. Save to file")  
                print("3. Done")  
                
                choice = input("\nSelect option (1-3): ").strip()  
                
                if choice == '1':  
                    print("\n=== Complete Message ===")  
                    print("-" * PREVIEW_LINE_LENGTH)  
                    for line in formatted_lines:  
                        print(line)  
                    print("-" * PREVIEW_LINE_LENGTH)  
                    
                elif choice == '2':  
                    try:  
                        default_filename = f"decrypted_{timestamp}.txt"  
                        save_filename = input(f"\nOutput filename [{default_filename}]: ").strip()  
                        
                        if not save_filename:  
                            save_filename = default_filename  
                        elif not save_filename.endswith('.txt'):  
                            save_filename += '.txt'  
                            
                        with open(save_filename, 'w', encoding='utf-8') as f:  
                            for line in formatted_lines:  
                                f.write(line + '\n')  
                                
                        print(f"\nMessage successfully saved to: {save_filename}")  
                        
                    except Exception as e:  
                        print(f"\nFailed to save file: {str(e)}")  
                        
                elif choice == '3':  
                    break  
                    
                else:  
                    print("\nInvalid choice!")  

            return decrypted_text  

        except FileNotFoundError:  
            print(f"\nFile not found: {filename}")  
            return None  
        except Exception as e:  
            logging.error(f"Decryption error: {str(e)}")  
            return None  

    def run(self):  
        """Run the QKD simulator"""  
        print("\n=== Enhanced Quantum Key Distribution Simulator ===")  
        print("Warning: The key can only be used once for maximum security")  
        
        while True:  
            try:  
                print("\nMenu:")  
                print("1. Generate New Quantum Key")  
                print("2. Encrypt & Share Message")   
                print("3. Decrypt Shared Message")  
                print("4. Exit")  
                
                choice = input("\nSelect menu (1-4): ").strip()  
                
                if choice == '1':  
                    print("\nGenerating new quantum key...")  
                    key, error_rate = self.bb84.generate_key()  
                    if key:  
                        self.current_key = key  
                        self.key_hash = hashlib.sha256(''.join(map(str, key)).encode()).hexdigest()  
                        self.use_count = 0  
                        print(f"\nSuccessfully generated key ({len(key)} bits)")  
                        print(f"Error rate: {error_rate:.2%}")  
                        print(f"Key hash: {self.key_hash[:16]}...")  
                    else:  
                        print("\nFailed to generate key - Try again")  
                
                elif choice == '2':  
                    print("\nMessage input mode:")  
                    print("1. Input directly with enter")  
                    print("2. Input from file")  
                    
                    input_mode = input("\nSelect mode (1-2): ").strip()  
                    
                    if input_mode == '1':  
                        filename, recovery_code = self.encrypt_and_share()  
                    elif input_mode == '2':  
                        file_path = input("\nEnter file path: ").strip()  
                        try:  
                            with open(file_path, 'r', encoding='utf-8') as f:  
                                message = f.read()  
                            filename, recovery_code = self.encrypt_and_share(message)  
                        except Exception as e:  
                            print(f"\nFailed to read file: {str(e)}")  
                            continue  
                    else:  
                        print("\nInvalid choice!")  
                        continue  
                    
                    if filename and recovery_code:  
                        print("\n=== Encryption Successful ===")  
                        print(f"1. Encryption file: {filename}")  
                        print(f"2. Recovery Code: {recovery_code}")  
                        print("\nInstructions for recipient:")  
                        print("1. Send .qk file via secure channel (ex: USB)")  
                        print("2. Send recovery code via different channel (ex: SMS)")  
                        print("\nWARNING: DO NOT send both through the same channel!")  
                    else:  
                        print("\nEncryption failed - Please try again")  
                
                elif choice == '3':  
                    print("\nDecrypt Message")  
                    print("-" * PREVIEW_LINE_LENGTH)  
                    
                    filename = input("\nEnter filename (.qk): ").strip()  
                    if not filename.endswith('.qk'):  
                        filename += '.qk'  
                        
                    recovery_code = input("Enter recovery code: ").strip()  
                    
                    if not filename or not recovery_code:  
                        print("\nFile name and recovery code must be filled in!")  
                        continue  
                        
                    decrypted = self.decrypt_shared_message(filename, recovery_code)  
                    if not decrypted:  
                        print("\nDecryption failed - Check file and recovery code")  
                
                elif choice == '4':  
                    print("\nThank you for using the QKD simulator!")  
                    break  
                
                else:  
                    print("\nInvalid choice!")  
                    
            except KeyboardInterrupt:  
                print("\n\nProgram stopped")  
                break  
            except Exception as e:  
                logging.error(f"Runtime error: {str(e)}")  
                print("\nAn error occurred, please try again")  

def main():  
    """Main functions of the program"""  
    try:  
        # Set seed for reproducibility  
        seed = int.from_bytes(  
            hashlib.sha256(  
                str(datetime.now().timestamp()).encode()  
            ).digest(),   
            'big'  
        )  
        random.seed(seed)  
        
        # Run the simulator  
        simulator = EnhancedQKDSimulator()  
        simulator.run()  
        
    except KeyboardInterrupt:  
        print("\n\nProgram stopped by user")  
    except Exception as e:  
        logging.critical(f"Critical error: {str(e)}")  
        print("\nA fatal error occurred. The program was terminated for safety reasons.")  

if __name__ == "__main__":  
    main()
