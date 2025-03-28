import requests
import pandas as pd
from datetime import datetime
import random
import numpy as np
import json
import os
import subprocess
import math

class ECommerceAPI:
    def __init__(self, use_local_api=False):
        self.use_local_api = use_local_api
        self.api_url = "http://localhost:3000/products"
        
        # Eğer yerel API kullanılacaksa, JSON dosyasını oluştur ve sunucuyu başlat
        if self.use_local_api:
            self._create_json_data()
            self._start_json_server()
        else:
            # Simüle edilmiş veri oluşturma
            self.data, _ = self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Örnek veri oluşturma"""
        # Kategori bazlı ürünler (her kategoride birden fazla ürün)
        category_products = {
            'Elektronik': ['Laptop', 'Akıllı Telefon', 'Tablet', 'Kulaklık', 'Monitör', 'Klavye', 'Mouse', 'Kamera'],
            'Giyim': ['T-shirt', 'Pantolon', 'Elbise', 'Gömlek', 'Ceket', 'Ayakkabı', 'Çanta', 'Şapka'],
            'Kitap': ['Roman', 'Bilim Kurgu', 'Tarih', 'Biyografi', 'Kişisel Gelişim', 'Çocuk Kitabı', 'Dergi', 'Akademik'],
            'Spor': ['Futbol Topu', 'Koşu Ayakkabısı', 'Fitness Ekipmanı', 'Bisiklet', 'Yüzme Gözlüğü', 'Tenis Raketi', 'Yoga Matı', 'Spor Çantası'],
            'Ev & Yaşam': ['Mobilya', 'Mutfak Eşyası', 'Yatak Örtüsü', 'Aydınlatma', 'Dekorasyon', 'Halı', 'Perde', 'Ev Tekstili'],
            'Kozmetik': ['Parfüm', 'Ruj', 'Fondöten', 'Şampuan', 'Krem', 'Güneş Kremi', 'Makyaj Seti', 'Saç Bakım Ürünü'],
            'Oyuncak': ['Lego', 'Peluş Oyuncak', 'Puzzle', 'Oyun Konsolu', 'Kutu Oyunu', 'Bebek', 'Uzaktan Kumandalı Araba', 'Eğitici Oyuncak'],
            'Bahçe': ['Bitki', 'Bahçe Mobilyası', 'Çim Biçme Makinesi', 'Sulama Sistemi', 'Tohum', 'Saksı', 'Bahçe Aletleri', 'Gübre'],
            'Otomotiv': ['Araç Aksesuarı', 'Oto Parfümü', 'Lastik', 'Yağ', 'Araç Bakım Ürünü', 'Navigasyon Cihazı', 'Araç Şarj Cihazı', 'Koltuk Kılıfı'],
            'Kırtasiye': ['Kalem', 'Defter', 'Dosya', 'Hesap Makinesi', 'Çanta', 'Takvim', 'Ajanda', 'Boya Seti']
        }
        
        # Kategori bazlı fiyat aralıkları (daha gerçekçi)
        category_price_ranges = {
            'Elektronik': (500, 5000),
            'Giyim': (50, 500),
            'Kitap': (20, 150),
            'Spor': (100, 2000),
            'Ev & Yaşam': (100, 3000),
            'Kozmetik': (30, 300),
            'Oyuncak': (50, 500),
            'Bahçe': (100, 2000),
            'Otomotiv': (50, 1000),
            'Kırtasiye': (5, 100)
        }
        
        # Müşteri sayısı
        n_customers = 20  # Müşteri sayısını artırdık
        
        # Toplam satış sayısı (her müşteri her kategoriden rastgele 2-4 ürün alsın)
        n_sales = 0  # Başlangıçta 0, dinamik olarak hesaplanacak
        
        # Müşteri bilgileri
        customers = []
        for i in range(1, n_customers + 1):
            customer = {
                'id': i,
                'name': f"Müşteri {i}",
                'email': f"musteri{i}@example.com",
                'age': random.randint(18, 75),
                'gender': random.choice(['Erkek', 'Kadın', 'Belirtilmemiş']),
                'address': f"Adres {i}"
            }
            customers.append(customer)
        
        # Satış verileri
        data = {
            'id': [],
            'customer_id': [],
            'product_name': [],
            'category': [],
            'price': [],
            'purchase_date': [],
            'quantity': [],
            'satisfaction_score': [],
            'payment_method': [],
            'shipping_cost': [],
            'discount_applied': []
        }
        
        # Ödeme yöntemleri
        payment_methods = ['Kredi Kartı', 'Havale', 'Kapıda Ödeme', 'Mobil Ödeme', 'Kripto Para']
        
        # Veri oluşturma - her müşteri her kategoriden rastgele 2-4 ürün alsın
        sale_id = 1
        for customer in customers:
            for category, products in category_products.items():
                # Her kategoriden kaç ürün alacak
                n_products_to_buy = random.randint(2, 4)
                
                # Rastgele ürünler seç
                selected_products = random.sample(products, min(n_products_to_buy, len(products)))
                
                for product in selected_products:
                    # ID
                    data['id'].append(sale_id)
                    
                    # Müşteri ID
                    data['customer_id'].append(customer['id'])
                    
                    # Ürün ve kategori
                    data['category'].append(category)
                    data['product_name'].append(product)
                    
                    # Fiyat (kategori bazlı)
                    min_price, max_price = category_price_ranges[category]
                    price = round(random.uniform(min_price, max_price), 2)
                    data['price'].append(price)
                    
                    # Tarih
                    date = (datetime.now() - pd.Timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
                    data['purchase_date'].append(date)
                    
                    # Miktar
                    data['quantity'].append(random.randint(1, 5))
                    
                    # Memnuniyet puanı
                    data['satisfaction_score'].append(round(random.uniform(1, 5), 1))
                    
                    # Ek alanlar
                    data['payment_method'].append(random.choice(payment_methods))
                    data['shipping_cost'].append(round(random.uniform(0, 50), 2))
                    data['discount_applied'].append(random.choice([True, False]))
                    
                    sale_id += 1
        
        # Toplam satış sayısını güncelle
        n_sales = len(data['id'])
        
        # DataFrame oluşturma
        df = pd.DataFrame(data)
        
        # Eksik veri ekleme (gerçekçi olması için)
        # Satışların %5'inde eksik veri olsun
        missing_indices = random.sample(range(n_sales), int(n_sales * 0.05))
        
        for idx in missing_indices:
            # Rastgele bir alan seç ve eksik bırak (quantity hariç)
            field = random.choice(['price', 'product_name', 'purchase_date', 'satisfaction_score'])
            df.loc[idx, field] = None
        
        # Satisfaction score için daha fazla eksik veri oluştur (satışların %15'i)
        satisfaction_missing_indices = random.sample(range(n_sales), int(n_sales * 0.15))
        for idx in satisfaction_missing_indices:
            df.loc[idx, 'satisfaction_score'] = None
            
        # Bazı ürünlerin fiyatlarını değişken yap (aynı ürün farklı fiyatlarda olabilir)
        # Bu, fiyat analizini daha ilginç hale getirecek
        for category, products in category_products.items():
            for product in products:
                # Bu ürünün satışlarını bul
                product_indices = df[df['product_name'] == product].index.tolist()
                
                if len(product_indices) > 1:
                    # Fiyat varyasyonu ekle (±%10)
                    for idx in product_indices:
                        if random.random() < 0.3:  # %30 olasılıkla fiyatı değiştir
                            current_price = df.loc[idx, 'price']
                            if pd.notna(current_price):
                                variation = random.uniform(0.9, 1.1)  # %10 yukarı veya aşağı
                                df.loc[idx, 'price'] = round(current_price * variation, 2)
        
        return df, customers
    
    def _create_json_data(self):
        """Dinamik olarak oluşturulan veriyi JSON dosyasına kaydetme"""
        # Veriyi oluştur
        df, customers = self._generate_sample_data()
        
        # NaN değerleri None olarak değiştir (JSON serileştirme için)
        df = df.where(pd.notna(df), None)
        
        # DataFrame'i JSON formatına dönüştür
        products_data = []
        
        for _, row in df.iterrows():
            # NaN değerleri kontrol et
            quantity = None if pd.isna(row['quantity']) else int(row['quantity'])
            price = None if pd.isna(row['price']) else float(row['price'])
            satisfaction_score = None if pd.isna(row['satisfaction_score']) else float(row['satisfaction_score'])
            
            product = {
                'id': int(row['id']),
                'customer_id': int(row['customer_id']),
                'product_name': row['product_name'],
                'category': row['category'],
                'price': price,
                'purchase_date': row['purchase_date'],
                'quantity': quantity,
                'satisfaction_score': satisfaction_score,
                'payment_method': row['payment_method'],
                'shipping_cost': float(row['shipping_cost']),
                'discount_applied': bool(row['discount_applied'])
            }
            products_data.append(product)
        
        # Kategori verisi oluştur
        categories_data = [
            {'id': 1, 'name': 'Elektronik', 'description': 'Elektronik ürünler ve aksesuarlar'},
            {'id': 2, 'name': 'Giyim', 'description': 'Kıyafet ve moda ürünleri'},
            {'id': 3, 'name': 'Kitap', 'description': 'Kitaplar ve dergiler'},
            {'id': 4, 'name': 'Spor', 'description': 'Spor ekipmanları ve giyim'},
            {'id': 5, 'name': 'Ev & Yaşam', 'description': 'Ev dekorasyon ve mobilya ürünleri'},
            {'id': 6, 'name': 'Kozmetik', 'description': 'Kozmetik ve kişisel bakım ürünleri'},
            {'id': 7, 'name': 'Oyuncak', 'description': 'Çocuk oyuncakları ve oyunları'},
            {'id': 8, 'name': 'Bahçe', 'description': 'Bahçe ekipmanları ve bitkileri'},
            {'id': 9, 'name': 'Otomotiv', 'description': 'Araç aksesuarları ve bakım ürünleri'},
            {'id': 10, 'name': 'Kırtasiye', 'description': 'Ofis ve okul malzemeleri'}
        ]
        
        # JSON dosyasını oluştur
        json_data = {
            'products': products_data,
            'customers': customers,
            'categories': categories_data
        }
        
        # JSON dosyasına kaydet
        with open('db.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print("JSON veri dosyası oluşturuldu: db.json")
        
        # Veriyi DataFrame olarak sakla
        self.data = df
    
    def _start_json_server(self):
        """JSON Server'ı başlatma"""
        try:
            # JSON Server'ın kurulu olup olmadığını kontrol et
            print("JSON Server kontrol ediliyor...")
            
            # package.json dosyasını oluştur
            if not os.path.exists('package.json'):
                package_json = {
                    "name": "ecommerce-api",
                    "version": "1.0.0",
                    "description": "E-Ticaret API",
                    "scripts": {
                        "start": "json-server --watch db.json --port 3000"
                    },
                    "dependencies": {
                        "json-server": "^0.17.4"
                    }
                }
                
                with open('package.json', 'w') as f:
                    json.dump(package_json, f, indent=2)
                
                print("package.json dosyası oluşturuldu.")
            
            print("JSON Server başlatılıyor...")
            print("API şu adreste çalışacak: http://localhost:3000")
            print("Postman ile bu adrese istek yapabilirsiniz.")
            print("Örnek endpoint'ler:")
            print("- Tüm ürünler: GET http://localhost:3000/products")
            print("- Tek ürün: GET http://localhost:3000/products/1")
            print("- Ürün filtreleme: GET http://localhost:3000/products?category=Elektronik")
            print("- Müşteriler: GET http://localhost:3000/customers")
            print("- Kategoriler: GET http://localhost:3000/categories")
            
            # Kullanıcıya JSON Server'ı nasıl başlatacağını göster
            print("\nJSON Server'ı başlatmak için terminal/komut isteminde şu komutu çalıştırın:")
            print("npx json-server --watch db.json --port 3000")
            
        except Exception as e:
            print(f"JSON Server başlatılırken hata oluştu: {e}")
            print("Lütfen manuel olarak şu komutu çalıştırın: npx json-server --watch db.json --port 3000")
    
    def fetch_data(self):
        """Veriyi API'den çekme"""
        if self.use_local_api:
            try:
                # API'den veri çekme
                print("API'den veri çekiliyor...")
                print(self.api_url)
                response = requests.get(self.api_url)
                if response.status_code == 200:
                    data = response.json()
                    return pd.DataFrame(data)
                else:
                    print(f"API'den veri çekilemedi. Hata kodu: {response.status_code}")
                    print("Simüle edilmiş veri kullanılıyor...")
                    return self._generate_sample_data()[0]  # Sadece DataFrame'i döndür
            except Exception as e:
                print(f"API bağlantısında hata: {e}")
                print("Simüle edilmiş veri kullanılıyor...")
                return self._generate_sample_data()[0]  # Sadece DataFrame'i döndür
        else:
            # Simüle edilmiş veriyi kullan
            return self.data
    
    def update_price(self, product_name, new_price):
        """Ürün fiyatını güncelleme"""
        if self.use_local_api:
            try:
                # Önce ürünü bul
                response = requests.get(f"{self.api_url}?product_name={product_name}")
                if response.status_code == 200:
                    products = response.json()
                    if products:
                        for product in products:
                            # Ürün fiyatını güncelle
                            product_id = product['id']
                            update_data = {'price': new_price}
                            update_response = requests.patch(f"{self.api_url}/{product_id}", json=update_data)
                            
                            if update_response.status_code == 200:
                                print(f"{product_name} ürününün fiyatı {new_price} olarak güncellendi.")
                            else:
                                print(f"Ürün fiyatı güncellenemedi. Hata kodu: {update_response.status_code}")
                    else:
                        print(f"{product_name} adlı ürün bulunamadı.")
                else:
                    print(f"API'den veri çekilemedi. Hata kodu: {response.status_code}")
            except Exception as e:
                print(f"API bağlantısında hata: {e}")
        else:
            # Simüle edilmiş veride güncelleme
            self.data.loc[self.data['product_name'] == product_name, 'price'] = new_price 