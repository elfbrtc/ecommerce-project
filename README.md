# E-Ticaret Veri Analizi Projesi

Bu proje, e-ticaret verilerinin analizi ve ürün öneri sistemi geliştirmeyi içermektedir.

## Kurulum Adımları

### Gereksinimler
- Python 3.8+
- Node.js ve npm

### 1. Projeyi İndirin
```bash
git clone [GITHUB_REPO_URL]
cd [PROJE_KLASÖRÜ]
```

### 2. Python Bağımlılıklarını Yükleyin
```bash
pip install -r requirements.txt
```

### 3. JSON Server'ı Yükleyin
```bash
npm install -g json-server
```

### 4. Projeyi Çalıştırın

#### 4.1. JSON Server'ı Başlatın
Yeni bir terminal açın ve aşağıdaki komutu çalıştırın:
```bash
npx json-server --watch db.json --port 3000
```

#### 4.2. Uygulamayı Çalıştırın
Başka bir terminal açın ve aşağıdaki komutu çalıştırın:
```bash
python main.py --use-api
```

## API Kullanımı

JSON Server çalıştıktan sonra aşağıdaki endpoint'lere erişebilirsiniz:

- Tüm ürünler: GET http://localhost:3000/products
- Tek ürün: GET http://localhost:3000/products/1
- Ürün filtreleme: GET http://localhost:3000/products?category=Elektronik
- Müşteriler: GET http://localhost:3000/customers
- Kategoriler: GET http://localhost:3000/categories

## Proje Yapısı

- `main.py`: Ana program dosyası
- `data_processor.py`: Veri işleme modülü
- `api_client.py`: API iletişim modülü
- `requirements.txt`: Python bağımlılıkları
- `db.json`: API için veri dosyası
- `package.json`: Node.js bağımlılıkları

## Kullanılan Teknolojiler

- Python 3.8+
- Pandas
- NumPy
- scikit-learn
- Matplotlib
- Seaborn 