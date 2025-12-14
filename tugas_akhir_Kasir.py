import os
import time

# --- PENGATURAN TAMPILAN (WARNA) ---
class Warna:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

# --- DATA daftar barang ---
daftar_barang = [
    {"nama": "Binder",      "harga": 15000},
    {"nama": "Tas Ransel",  "harga": 150000},
    {"nama": "Tumbler",     "harga": 25000},
    {"nama": "Pulpen",      "harga": 5000},
    {"nama": "Spidol",      "harga": 8000}
]
keranjang = []
nama_pelanggan = ""  # Variabel Global

# --- FUNGSI BANTUAN ---
#agar angka jadi berkoma/desimal
def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def bersihkan_layar():
    os.system('cls')

def header_aplikasi():
    #Menampilkan Header dengan Nama Pelanggan
    print(Warna.HEADER + Warna.BOLD + "="*50)
    print("      U N J A   M A R T   S H O P      ")
    print("="*50 + Warna.END)
    if nama_pelanggan:
        print(f"Pelanggan : {Warna.CYAN}{nama_pelanggan}{Warna.END}")
        print("-" * 50)

# --- FUNGSI UTAMA ---
#jika pilih tambah pesanan maka fungsi di bawah akan dijalankan
def tambah_pesanan():
    bersihkan_layar()
    header_aplikasi()
    print(f"\n{Warna.CYAN}[ DAFTAR BARANG TERSEDIA ]{Warna.END}")
    #menampilkan barang yang tersedia
    print("-" * 50)
    print(f"| {'No':<3} | {'Nama Barang':<20} | {'Harga':>15} |")
    print("-" * 50)
    #enumarate mengambil index dari daftar barang
    for i, item in enumerate(daftar_barang):
        print(f"| {i+1:<3} | {item['nama']:<20} | {format_rupiah(item['harga']):>15} |")
    print("-" * 50)

    while True:
        try:
            print(f"\n{Warna.WARNING}Ketik 0 untuk kembali ke menu utama{Warna.END}")
            pilihan = int(input(f"{Warna.BOLD}>> Pilih Nomor Barang: {Warna.END}"))
            #jiks pilih 0 lansung balik ke menu awal
            if pilihan == 0: break
            #jika pilihan 1 - 5
            if 1 <= pilihan <= len(daftar_barang):
                item = daftar_barang[pilihan - 1]
                qty = int(input(f"   Jumlah {Warna.CYAN}{item['nama']}{Warna.END}: "))
                
                if qty > 0:
                    keranjang.append({ #menambahkan item ke keranjang untuk di hitung
                        "nama": item['nama'],
                        "harga_satuan": item['harga'],
                        "qty": qty,
                        "subtotal": item['harga'] * qty
                    })
                    print(f"\n{Warna.GREEN}[+] Berhasil menambahkan {qty} {item['nama']} ke keranjang!{Warna.END}")
                    time.sleep(1)
                    break 
            else:
                print(f"{Warna.FAIL}[!] Barang tidak ditemukan.{Warna.END}")
        except ValueError:
            print(f"{Warna.FAIL}[!] Input harus berupa angka.{Warna.END}")

def hitung_bayar():
    """Mengembalikan True jika pembayaran sukses, False jika batal/gagal"""
    if not keranjang:
        print(f"\n{Warna.FAIL}[!] Keranjang masih kosong. Belanja dulu yuk!{Warna.END}")
        time.sleep(1.5)
        return False # Transaksi belum terjadi
    #lalu layar di bersihkan kembali dengan fungsi 'cls'
    bersihkan_layar()
    header_aplikasi()
    print(f"\n{Warna.BLUE}[ KASIR & PEMBAYARAN ]{Warna.END}")
    
    print("-" * 50)
    print(f"| {'Nama Barang':<18} | {'Qty':<3} | {'Subtotal':>18} |")
    print("-" * 50)
    
    total = 0 # total masih 0 akan di jumlah kan jika isi keranjang ada total+=item
    for item in keranjang:
        print(f"| {item['nama']:<18} | {item['qty']:<3} | {format_rupiah(item['subtotal']):>18} |")
        total += item['subtotal']
    
    print("-" * 50)
    print(f"{Warna.BOLD}TOTAL TAGIHAN: {format_rupiah(total)}{Warna.END}".rjust(58)) 
    print("-" * 50)
    
    print(f"\n{Warna.WARNING}(Ketik 0 untuk membatalkan transaksi){Warna.END}")
    #perulangan true untuk menghitung pembayaran 
    while True:
        try:
            bayar = int(input(f"{Warna.BOLD}>> Masukkan Uang Bayar: Rp {Warna.END}"))
            
            if bayar == 0:
                print(f"\n{Warna.FAIL}[X] Pembayaran Dibatalkan.{Warna.END}")
                time.sleep(1.5)
                return False # Transaksi batal kembali ke menu awal
                #pembayaran nya selesai uang mencukupi
            if bayar >= total:
                kembalian = bayar - total
                print(f"\n{Warna.GREEN}=== TRANSAKSI BERHASIL ==={Warna.END}")
                print(f"Pelanggan : {nama_pelanggan}")
                print(f"Total     : {format_rupiah(total)}")
                print(f"Diterima  : {format_rupiah(bayar)}")
                print(f"Kembalian : {format_rupiah(kembalian)}")
                print("==== HAPPY SHOPPING ====")
                # lalu keranjang di bersihkan kembali
                keranjang.clear()
                input(f"\n{Warna.BOLD}[ Tekan Enter untuk transaksi baru... ]{Warna.END}")
                return True # FOKUS: Transaksi Sukses!
            else: 
                print(f"{Warna.FAIL}[!] Uang kurang sebesar {format_rupiah(total - bayar)}{Warna.END}")
        except ValueError:
            print(f"{Warna.FAIL}[!] Harap masukkan angka saja.{Warna.END}")


# --- PROGRAM UTAMA ---
def main():
    global nama_pelanggan
    
    while True: # LOOP LUAR: Untuk Pelanggan Baru
        bersihkan_layar()
        
        # Reset nama jika looping ulang 
        nama_pelanggan = "" 
        
        print(Warna.HEADER + Warna.BOLD + "="*50)
        print("\t    U N J A   M A R T  S H O P      ")
        print("="*50 + Warna.END)
        print(f"{Warna.CYAN}Selamat Datang di Kasir{Warna.END}")
        
        # Input Nama Pelanggan Baru di sini
        nama_pelanggan = input(f"{Warna.BOLD}>> Masukkan Nama Pelanggan: {Warna.END}")
        
        # Loop Menu Transaksi (Pelanggan yang sama)
        while True: 
            bersihkan_layar()
            header_aplikasi()
            
            print(f"{Warna.CYAN}Menu Utama:{Warna.END}\n")
            print(f"[1] {Warna.GREEN}Tambah Pesanan{Warna.END}")
            print(f"[2] {Warna.BLUE}Bayar / Checkout{Warna.END}")
            print(f"[3] {Warna.FAIL}Keluar Aplikasi{Warna.END}")
            print("-" * 50)
            
            barang = input(f"{Warna.BOLD}>> Masukkan Pilihan [1-3]: {Warna.END}")
            #memilih pesanan
            if barang == '1':
                tambah_pesanan()
            elif barang == '2':
                # Cek status pembayaran
                status_bayar = hitung_bayar()
                
                # FOKUS: Jika status_bayar adalah True (Sukses), keluar dari loop menu
                if status_bayar == True:
                    break # Break ini akan melempar kita ke Loop Luar
                    
            elif barang == '3':
                print(f"\n{Warna.HEADER}Terima kasih {nama_pelanggan}, sampai jumpa!{Warna.END}")
                return # Keluar dari seluruh program (stop total)
            else:
                print(f"{Warna.FAIL}Pilihan tidak valid.{Warna.END}")
                time.sleep(1)
#program otomatis berjalan ketika file .py dibuka
if __name__ == "__main__":
    main()