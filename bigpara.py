import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime  # Tarih ve saat için gerekli

def get_dollar_rate():
    try:
        url = "https://bigpara.hurriyet.com.tr/doviz/dolar/"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Hata durumunda exception fırlatır

        soup = BeautifulSoup(response.text, 'html.parser')
        rate_element = soup.find("span", class_="value")

        if rate_element:
            return rate_element.text.strip()
        else:
            return None
    except Exception as e:
        return None

def update_rate():
    rate = get_dollar_rate()
    if rate:
        # Güncel tarih ve saati al
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y %H:%M:%S")  # Örnek format: 12.07.2004 14:35:07
        result = f"{date_time} - Dolar Kuru: {rate} TL"
        result_label.config(text=result)

        # Masaüstüne kaydet
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        file_path = os.path.join(desktop, "dolar_kuru.txt")
        with open(file_path, "a", encoding="utf-8") as file:  # "a" ile dosya sonuna ekleme yapar
            file.write(result + "\n")

        messagebox.showinfo("Bilgi", f"Dolar kuru masaüstüne kaydedildi: {file_path}")
    else:
        messagebox.showerror("Hata", "Dolar kuru bilgisi alınamadı.")

# Tkinter arayüzü oluştur
root = tk.Tk()
root.title("Dolar Kuru Takip")
root.geometry("400x200")

# Başlık
title_label = tk.Label(root, text="Güncel Dolar Kuru", font=("Helvetica", 16))
title_label.pack(pady=10)

# Sonuç Label
result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.pack(pady=10)

# Güncelle Butonu
update_button = tk.Button(root, text="Kuru Güncelle", font=("Helvetica", 12), command=update_rate)
update_button.pack(pady=10)

# Uygulamayı çalıştır
root.mainloop()