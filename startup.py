# Onur Altan Uyar
# Dosya Ekleme (.py)

import os
import shutil
from datetime import datetime

def should_backup(src, dest):
    """Dosya mevcut değilse veya değişmişse True döner."""
    if not os.path.exists(dest):
        return True
    src_stat = os.stat(src)
    dest_stat = os.stat(dest)
    # Dosya boyutu veya değiştirilme zamanı farklıysa yedekle
    if src_stat.st_size != dest_stat.st_size or src_stat.st_mtime > dest_stat.st_mtime:
        return True
    return False

def backup_folder(source_folder, backup_folder, extensions=None):
    if not os.path.exists(source_folder):
        print(f"{source_folder} bulunamadı.")
        return

    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join(backup_folder, f"backup_{date_str}")
    os.makedirs(backup_path, exist_ok=True)

    log_entries = []

    for foldername, subfolders, filenames in os.walk(source_folder):
        relative_path = os.path.relpath(foldername, source_folder)
        dest_folder = os.path.join(backup_path, relative_path)
        os.makedirs(dest_folder, exist_ok=True)

        for filename in filenames:
            if extensions and not filename.lower().endswith(tuple(extensions)):
                continue
            src_file = os.path.join(foldername, filename)
            dest_file = os.path.join(dest_folder, filename)
            if should_backup(src_file, dest_file):
                shutil.copy2(src_file, dest_file)
                log_entries.append(f"{datetime.now()}: Yedeklendi - {src_file} -> {dest_file}")
                print(f"Yedeklendi: {src_file} -> {dest_file}")
            else:
                print(f"Atlandı (değişmedi): {src_file}")

    # Log dosyasını yaz
    log_file = os.path.join(backup_path, "backup_log.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(log_entries))

    print(f"Yedekleme tamamlandı! Log dosyası: {log_file}")

if __name__ == "__main__":
    source = input("Yedeklenecek klasörün tam yolu: ")
    backup = input("Yedeklerin kaydedileceği klasörün tam yolu: ")
    ext_input = input("Yedeklenecek dosya türleri (örnek: txt,py) veya boş bırak tümünü yedekle: ")
    extensions = [e.strip().lower() for e in ext_input.split(",")] if ext_input else None

    backup_folder(source, backup, extensions)
