import os
import random  
import logging  
import hashlib  
import math  
import time  
from datetime import datetime  
from typing import List, Tuple, Optional  

if os.name == 'nt':  # For Windows  
    os.system('title توزيع المفتاح الكمومي')  
else:  # For Unix/Linux/Mac  
    print("\033]0;توزيع المفتاح الكمومي\007")

# الثوابت  
PREVIEW_LINE_LENGTH = 50  
PROGRESS_BAR_LENGTH = 30  

# إعداد السجلات  
logging.basicConfig(  
    level=logging.WARNING,  
    format='%(asctime)s - %(levelname)s: %(message)s',  
    datefmt='%Y-%m-%d %H:%M:%S'  
)  

def show_progress(current: int, total: int, prefix: str = '', suffix: str = ''):  
    """عرض شريط التقدم مع النسبة المئوية"""  
    filled = int(round(PROGRESS_BAR_LENGTH * current / float(total)))  
    bar = '=' * filled + '-' * (PROGRESS_BAR_LENGTH - filled)  
    percent = round(100.0 * current / float(total), 1)  
    print(f'\r{prefix} [{bar}] {percent}% {suffix}', end='\r')  
    if current == total:  
        print()  

class SecureBB84:  
    """تنفيذ بروتوكول BB84 للتوزيع المفتاح الكمي"""  
    def __init__(self):  
        self.bases = ['مستقيم', 'قطري']  
        self.error_threshold = 0.15  
        self.num_qubits = 1000000  
        self.min_key_length = 500  
        self.verification_bits = 40  
        self.noise_threshold = 0.95  
        self.chunk_size = 1000  

    def secure_random(self) -> int:  
        """توليد بت عشوائي آمن"""  
        return random.getrandbits(1)  

    def simulate_transmission(self, bit: int, send_basis: str, receive_basis: str) -> Tuple[int, float]:  
        """محاكاة نقل الكيوبت"""  
        if send_basis == receive_basis:  
            return bit, 1.0  
        return self.secure_random(), 0.5  

    def verify_key_security(self, key: List[int]) -> bool:  
        """التحقق من أمان المفتاح"""  
        if len(key) < self.min_key_length:  
            return False  
        ones = sum(key) / len(key)  
        return 0.3 <= ones <= 0.7  

    def generate_key(self) -> Tuple[Optional[List[int]], float]:  
        """توليد مفتاح كمي جديد"""  
        try:  
            retry_count = 0  
            max_retries = 3  
            
            while retry_count < max_retries:  
                print("\nجاري توليد البتات الكمية...")  
                alice_bits = [self.secure_random() for _ in range(self.num_qubits)]  
                alice_bases = [random.choice(self.bases) for _ in range(self.num_qubits)]  
                bob_bases = [random.choice(self.bases) for _ in range(self.num_qubits)]  
                
                received_bits = []  
                received_confidence = []  
                
                for i in range(self.num_qubits):  
                    bit, conf = self.simulate_transmission(  
                        alice_bits[i],  
                        alice_bases[i],  
                        bob_bases[i]  
                    )  
                    received_bits.append(bit)  
                    received_confidence.append(conf)  
                    
                    if i % 100 == 0:  
                        show_progress(i, self.num_qubits, 'توليد المفتاح الكمي: ')  
                
                show_progress(self.num_qubits, self.num_qubits, 'توليد المفتاح الكمي: ')  
                
                # تنقية المفتاح  
                sifted_key = []  
                verification_bits = []  
                errors = 0  
                total_matched = 0  
                
                print("\nجاري تنقية المفتاح الكمي...")  
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
                        show_progress(i, self.num_qubits, 'تنقية المفتاح: ')  
                
                show_progress(self.num_qubits, self.num_qubits, 'تنقية المفتاح: ')  
                
                if total_matched == 0:  
                    retry_count += 1  
                    continue  
                    
                error_rate = errors / total_matched  
                
                if len(sifted_key) >= self.min_key_length and error_rate <= self.error_threshold:  
                    return sifted_key, error_rate  
                    
                retry_count += 1  
                print(f"\nإعادة المحاولة {retry_count}/{max_retries} - معدل الخطأ مرتفع جداً")  
                
            return None, 1.0  
            
        except Exception as e:  
            logging.error(f"خطأ في توليد المفتاح: {str(e)}")  
            return None, 1.0

class EnhancedQKDSimulator:  
    """محاكي التوزيع المفتاح الكمي المحسن"""  
    def __init__(self):  
        self.bb84 = SecureBB84()  
        self.current_key = None  
        self.key_hash = None  
        self.use_count = 0  
        self.chunk_size = self.bb84.chunk_size  
        self.key_pool = []  

    def text_to_binary(self, text: str) -> str:  
        """تحويل النص إلى ثنائي مع الحفاظ على أسطر جديدة"""  
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
            logging.error(f"خطأ في تحويل النص إلى ثنائي: {str(e)}")  
            return None  

    def binary_to_text(self, binary: str) -> str:  
        """تحويل الثنائي إلى نص مع الحفاظ على أسطر جديدة"""  
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
            logging.error(f"خطأ في تحويل الثنائي إلى نص: {str(e)}")  
            return None  

    def generate_key_pool(self, needed_length: int) -> bool:  
        """توليد مجموعة مفاتيح كمية حسب الحاجة"""  
        try:  
            current_length = sum(len(k) for k in self.key_pool)  
            while current_length < needed_length:  
                print(f"\nتوليد مفاتيح إضافية ({current_length}/{needed_length} بت متوفر)")  
                key, error_rate = self.bb84.generate_key()  
                if not key:  
                    return False  
                self.key_pool.append(key)  
                current_length += len(key)  
                show_progress(current_length, needed_length, 'مجموعة المفاتيح: ')  
            return True  
        except Exception as e:  
            logging.error(f"خطأ في توليد مجموعة المفاتيح: {str(e)}")  
            return False  

    def get_key_from_pool(self, length: int) -> List[int]:  
        """الحصول على مفتاح من المجموعة حسب الطول المطلوب"""  
        result = []  
        while len(result) < length:  
            if not self.key_pool:  
                if not self.generate_key_pool(length - len(result)):  
                    raise Exception("فشل في توليد مفاتيح كافية")  
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
        """إدخال متعدد الأسطر مع حد 4 إدخالات متتالية"""  
        enter_count = 0  
        message_lines = []  
        
        print("\nأدخل الرسالة (الحد الأقصى 4 سطور فارغة متتالية):")  
        print("اكتب 'إلغاء' في سطر جديد للإلغاء")  
        print("-" * PREVIEW_LINE_LENGTH)  
        
        while enter_count < 4:  
            try:  
                line = input()  
                
                if line == 'إلغاء':  
                    return None  
                    
                message_lines.append(line)  
                
                if line.strip() == '':  
                    enter_count += 1  
                else:  
                    enter_count = 0  
                    
            except KeyboardInterrupt:  
                print("\nتم إلغاء الإدخال!")  
                return None  
                
        return '\n'.join(message_lines)

    def encrypt_and_share(self, message: str = '') -> Tuple[Optional[str], Optional[str]]:  
        """تشفير وإعداد الرسالة للمشاركة"""  
        try:  
            if not message:  
                message = self.get_multiline_input()  
                
            if not message or message.isspace():  
                print("\nلا يمكن أن تكون الرسالة فارغة!")  
                return None, None  

            print("\nالرسالة التي سيتم تشفيرها:")  
            print("-" * PREVIEW_LINE_LENGTH)  
            lines = message.split('\n')  
            if len(lines) > 5:  
                for line in lines[:5]:  
                    print(line)  
                print(f"\n... {len(lines) - 5} أسطر أخرى ...")  
            else:  
                for line in lines:  
                    print(line)  
            print("-" * PREVIEW_LINE_LENGTH)  
            print(f"إجمالي الأسطر: {len(lines)}")  
            print(f"إجمالي الأحرف: {len(message)}")  
            
            if input("\nمتابعة التشفير؟ (ن/ي): ").lower() != 'ي':  
                return None, None  

            # تقسيم الرسالة إلى أجزاء  
            message_chunks = [  
                message[i:i+self.chunk_size]  
                for i in range(0, len(message), self.chunk_size)  
            ]  

            total_chunks = len(message_chunks)  
            print(f"\nمعالجة {total_chunks} جزء...")  

            encrypted_chunks = []  
            keys_used = []  

            # تشفير كل جزء  
            for i, chunk in enumerate(message_chunks, 1):  
                print(f"\nمعالجة الجزء {i}/{total_chunks}")  
                binary_chunk = self.text_to_binary(chunk)  
                if not binary_chunk:  
                    return None, None  

                chunk_length = len(binary_chunk)  
                
                try:  
                    chunk_key = self.get_key_from_pool(chunk_length)  
                except Exception as e:  
                    print("\nفشل في توليد المفتاح الكمي")  
                    return None, None  

                encrypted_bits = [  
                    str(int(a) ^ b)  
                    for a, b in zip(binary_chunk, chunk_key)  
                ]  
                encrypted_chunks.append(''.join(encrypted_bits))  
                keys_used.append(chunk_key)  
                
                show_progress(i, total_chunks, 'التشفير: ')  

            print("\nإنشاء مفتاح النقل...")  
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  
            salt = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()[:16]  
            transport_key = hashlib.pbkdf2_hmac(  
                'sha256',  
                salt.encode(),  
                timestamp.encode(),  
                100000  
            ).hex()[:32]  

            print("تشفير المفتاح...")  
            all_keys = []  
            for i, key in enumerate(keys_used, 1):  
                key_str = ','.join(map(str, key))  
                key_bytes = key_str.encode()  
                encrypted_key = [  
                    kb ^ int(transport_key[i % len(transport_key)], 16)  
                    for i, kb in enumerate(key_bytes)  
                ]  
                all_keys.append(''.join(map(lambda x: format(x, '02x'), encrypted_key)))  
                show_progress(i, len(keys_used), 'تشفير المفتاح: ')  

            print("\nتحضير البيانات للتصدير...")  
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
            
            print("حفظ الملف...")  
            with open(filename, 'w', encoding='utf-8') as f:  
                f.write(export_str)  

            recovery_code = hashlib.sha256(transport_key.encode()).hexdigest()[:12]  

            return filename, recovery_code  

        except Exception as e:  
            logging.error(f"خطأ في التشفير: {str(e)}")  
            return None, None  

    def decrypt_shared_message(self, filename: str, recovery_code: str) -> Optional[str]:  
        """فك تشفير الرسالة المشفرة"""  
        try:  
            print("\nقراءة الملف...")  
            with open(filename, 'r', encoding='utf-8') as f:  
                data = f.read().strip()  

            parts = data.split("@@@")  
            if len(parts) != 6:  
                print("\nتنسيق الملف غير صالح")  
                return None  

            timestamp, salt, encrypted_keys_str, encrypted_message, ver_hash, chunk_count = parts  
            chunk_count = int(chunk_count)  

            print("التحقق من سلامة الملف...")  
            check_hash = hashlib.sha256(  
                f"{timestamp}{salt}{encrypted_keys_str}{encrypted_message}".encode()  
            ).hexdigest()  

            if check_hash != ver_hash:  
                print("\nتحذير: تم تعديل الملف!")  
                if input("متابعة فك التشفير؟ (ن/ي): ").lower() != 'ي':  
                    return None

            print("إنشاء مفتاح النقل...")  
            transport_key = hashlib.pbkdf2_hmac(  
                'sha256',  
                salt.encode(),  
                timestamp.encode(),  
                100000  
            ).hex()[:32]  

            print("التحقق من رمز الاسترداد...")  
            check_code = hashlib.sha256(transport_key.encode()).hexdigest()[:12]  
            if check_code != recovery_code:  
                print("\nرمز الاسترداد غير صالح!")  
                return None  

            encrypted_keys = encrypted_keys_str.split("###")  
            encrypted_chunks = encrypted_message.split("###")  

            if len(encrypted_keys) != chunk_count or len(encrypted_chunks) != chunk_count:  
                print("\nبيانات الأجزاء غير صالحة")  
                return None  

            print(f"\nمعالجة {chunk_count} جزء...")  
            decrypted_chunks = []  
            
            for i in range(chunk_count):  
                try:  
                    # فك تشفير المفتاح  
                    encrypted_key_bytes = bytes.fromhex(encrypted_keys[i])  
                    decrypted_key = []  
                    for j, eb in enumerate(encrypted_key_bytes):  
                        tk_byte = int(transport_key[j % len(transport_key)], 16)  
                        decrypted_key.append(eb ^ tk_byte)  
                    key_str = bytes(decrypted_key).decode('utf-8', errors='ignore')  
                    chunk_key = [int(k) for k in key_str.split(',') if k.strip()]  

                    # فك تشفير جزء الرسالة  
                    decrypted_bits = [  
                        str(int(a) ^ b)  
                        for a, b in zip(encrypted_chunks[i], chunk_key)  
                    ]  
                    decrypted_binary = ''.join(decrypted_bits)  
                    decrypted_chunk = self.binary_to_text(decrypted_binary)  
                    
                    if decrypted_chunk:  
                        decrypted_chunks.append(decrypted_chunk)  
                    else:  
                        raise Exception(f"فشل في فك تشفير الجزء {i+1}")  
                        
                    show_progress(i+1, chunk_count, 'فك التشفير: ')  

                except Exception as e:  
                    logging.error(f"خطأ في فك تشفير الجزء {i+1}: {str(e)}")  
                    return None  

            decrypted_text = ''.join(decrypted_chunks)  
            formatted_lines = decrypted_text.split('\n')  

            print("\n=== الرسالة بعد فك التشفير ===")  
            print("-" * PREVIEW_LINE_LENGTH)  
            
            preview_lines = formatted_lines[:5]  
            for line in preview_lines:  
                print(line)  
                
            if len(formatted_lines) > 5:  
                print(f"\n... {len(formatted_lines) - 5} أسطر أخرى ...")  
            
            print("-" * PREVIEW_LINE_LENGTH)  
            print(f"إجمالي الأسطر: {len(formatted_lines)}")  
            print(f"إجمالي الأحرف: {len(decrypted_text)}")  

            while True:  
                print("\nالخيارات:")  
                print("١. عرض الرسالة كاملة")  
                print("٢. حفظ إلى ملف")  
                print("٣. إنهاء")  
                
                choice = input("\nاختر خياراً (١-٣): ").strip()  
                
                if choice == '١':  
                    print("\n=== الرسالة الكاملة ===")  
                    print("-" * PREVIEW_LINE_LENGTH)  
                    for line in formatted_lines:  
                        print(line)  
                    print("-" * PREVIEW_LINE_LENGTH)  
                    
                elif choice == '٢':  
                    try:  
                        default_filename = f"decrypted_{timestamp}.txt"  
                        save_filename = input(f"\nاسم ملف الحفظ [{default_filename}]: ").strip()  
                        
                        if not save_filename:  
                            save_filename = default_filename  
                        elif not save_filename.endswith('.txt'):  
                            save_filename += '.txt'  
                            
                        with open(save_filename, 'w', encoding='utf-8') as f:  
                            for line in formatted_lines:  
                                f.write(line + '\n')  
                                
                        print(f"\nتم حفظ الرسالة بنجاح في: {save_filename}")  
                        
                    except Exception as e:  
                        print(f"\nفشل في حفظ الملف: {str(e)}")  
                        
                elif choice == '٣':  
                    break  
                    
                else:  
                    print("\nخيار غير صالح!")  

            return decrypted_text  

        except FileNotFoundError:  
            print(f"\nالملف غير موجود: {filename}")  
            return None  
        except Exception as e:  
            logging.error(f"خطأ في فك التشفير: {str(e)}")  
            return None  

    def run(self):  
        """تشغيل محاكي توزيع المفتاح الكمي"""  
        print("\n=== محاكي توزيع المفتاح الكمي المتقدم ===")  
        print("تحذير: يجب استخدام المفتاح مرة واحدة فقط للأمان الأقصى")  
        
        while True:  
            try:  
                print("\nالقائمة:")  
                print("١. توليد مفتاح كمي جديد")  
                print("٢. تشفير ومشاركة رسالة")  
                print("٣. فك تشفير رسالة مشتركة")  
                print("٤. خروج")  
                
                choice = input("\nاختر من القائمة (١-٤): ").strip()  
                
                if choice == '١':  
                    print("\nتوليد مفتاح كمي جديد...")  
                    key, error_rate = self.bb84.generate_key()  
                    if key:  
                        self.current_key = key  
                        self.key_hash = hashlib.sha256(''.join(map(str, key)).encode()).hexdigest()  
                        self.use_count = 0  
                        print(f"\nتم توليد المفتاح بنجاح ({len(key)} بت)")  
                        print(f"معدل الخطأ: {error_rate:.2%}")  
                        print(f"تجزئة المفتاح: {self.key_hash[:16]}...")  
                    else:  
                        print("\nفشل في توليد المفتاح - حاول مرة أخرى")  
                
                elif choice == '٢':  
                    print("\nطريقة إدخال الرسالة:")  
                    print("١. إدخال مباشر")  
                    print("٢. إدخال من ملف")  
                    
                    input_mode = input("\nاختر الطريقة (١-٢): ").strip()  
                    
                    if input_mode == '١':  
                        filename, recovery_code = self.encrypt_and_share()  
                    elif input_mode == '٢':  
                        file_path = input("\nأدخل مسار الملف: ").strip()  
                        try:  
                            with open(file_path, 'r', encoding='utf-8') as f:  
                                message = f.read()  
                            filename, recovery_code = self.encrypt_and_share(message)  
                        except Exception as e:  
                            print(f"\nفشل في قراءة الملف: {str(e)}")  
                            continue  
                    else:  
                        print("\nخيار غير صالح!")  
                        continue  
                    
                    if filename and recovery_code:  
                        print("\n=== تم التشفير بنجاح ===")  
                        print(f"١. ملف التشفير: {filename}")  
                        print(f"٢. رمز الاسترداد: {recovery_code}")  
                        print("\nتعليمات للمستلم:")  
                        print("١. أرسل ملف .qk عبر قناة آمنة (مثل USB)")  
                        print("٢. أرسل رمز الاسترداد عبر قناة مختلفة (مثل SMS)")  
                        print("\nتحذير: لا ترسل كليهما عبر نفس القناة!")  
                    else:  
                        print("\nفشل التشفير - حاول مرة أخرى")  
                
                elif choice == '٣':  
                    print("\nفك تشفير الرسالة")  
                    print("-" * PREVIEW_LINE_LENGTH)  
                    
                    filename = input("\nأدخل اسم الملف (.qk): ").strip()  
                    if not filename.endswith('.qk'):  
                        filename += '.qk'  
                        
                    recovery_code = input("أدخل رمز الاسترداد: ").strip()  
                    
                    if not filename or not recovery_code:  
                        print("\nيجب إدخال اسم الملف ورمز الاسترداد!")  
                        continue  
                        
                    decrypted = self.decrypt_shared_message(filename, recovery_code)  
                    if not decrypted:  
                        print("\nفشل فك التشفير - تحقق من الملف ورمز الاسترداد")  
                
                elif choice == '٤':  
                    print("\nشكراً لاستخدام محاكي توزيع المفتاح الكمي!")  
                    break  
                
                else:  
                    print("\nخيار غير صالح!")  
                    
            except KeyboardInterrupt:  
                print("\n\nتم إيقاف البرنامج")  
                break  
            except Exception as e:  
                logging.error(f"خطأ في التشغيل: {str(e)}")  
                print("\nحدث خطأ، حاول مرة أخرى")  

def main():  
    """الدالة الرئيسية للبرنامج"""  
    try:  
        seed = int.from_bytes(  
            hashlib.sha256(  
                str(datetime.now().timestamp()).encode()  
            ).digest(),  
            'big'  
        )  
        random.seed(seed)  
        
        simulator = EnhancedQKDSimulator()  
        simulator.run()  
        
    except KeyboardInterrupt:  
        print("\n\nتم إيقاف البرنامج بواسطة المستخدم")  
    except Exception as e:  
        logging.critical(f"خطأ حرج: {str(e)}")  
        print("\nحدث خطأ فادح. تم إيقاف البرنامج للأمان.")  

if __name__ == "__main__":  
    main()