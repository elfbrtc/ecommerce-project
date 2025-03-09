from api_client import ECommerceAPI
from data_processor import DataProcessor
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def main():
    # Komut satırı argümanlarını ayarla
    parser = argparse.ArgumentParser(description='E-Ticaret Veri Analizi')
    parser.add_argument('--use-api', action='store_true', help='Yerel API kullan')
    args = parser.parse_args()
    
    # API'den veri çekme
    print("Veri çekiliyor...")
    api = ECommerceAPI(use_local_api=args.use_api)
    df = api.fetch_data()
    
    # Veri hakkında genel bilgi
    print("\nVeri seti hakkında genel bilgi:")
    print(f"Satır sayısı: {df.shape[0]}, Sütun sayısı: {df.shape[1]}")
    print("\nSütunlar:")
    for col in df.columns:
        print(f"- {col}")
    
    # Eksik veri analizi (işlemeden önce)
    print("\nEksik veri analizi (temizleme öncesi):")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    missing_df = pd.DataFrame({
        'Eksik Değer Sayısı': missing_data,
        'Eksik Değer Oranı (%)': missing_percent
    }).sort_values('Eksik Değer Sayısı', ascending=False)
    print(missing_df[missing_df['Eksik Değer Sayısı'] > 0])
    
    # Veri işleme
    print("\nVeri işleniyor...")
    processor = DataProcessor(df)
    
    # Eksik veri işleme sonuçları
    print("\nEksik veri temizleme sonuçları:")
    cleaning_comparison = processor.compare_before_after_cleaning()
    print(cleaning_comparison[cleaning_comparison['Temizleme Öncesi Eksik'] > 0])
    
    # Eksik veri görselleştirme
    print("\nEksik veri dağılımı görselleştiriliyor...")
    processor.plot_missing_data()
    
    # 1. En çok satın alınan ürünler
    print("\nEn çok satın alınan 10 ürün:")
    top_products = processor.analyze_top_products()
    print(top_products)
    
    # Görselleştirme
    plt.figure(figsize=(12, 6))
    top_products.plot(kind='bar')
    plt.title('En Çok Satın Alınan 10 Ürün')
    plt.xlabel('Ürün')
    plt.ylabel('Toplam Satış Miktarı')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # 2. Fiyat ve satış miktarı korelasyonu
    print("\nFiyat ve satış miktarı korelasyonu:")
    corr = processor.price_quantity_correlation()
    print(corr)
    
    # Görselleştirme
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Fiyat ve Satış Miktarı Korelasyonu')
    plt.tight_layout()
    plt.show()
    
    # 3. Kategori bazlı fiyat analizi
    print("\nKategori bazlı fiyat analizi:")
    category_prices = processor.category_price_analysis()
    print(category_prices)
    
    # Görselleştirme
    plt.figure(figsize=(12, 6))
    category_prices['mean'].plot(kind='bar')
    plt.title('Kategorilere Göre Ortalama Fiyatlar')
    plt.xlabel('Kategori')
    plt.ylabel('Ortalama Fiyat (TL)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # 4. Son 30 günlük satış analizi
    print("\nSon 30 günlük en çok satılan ürünler:")
    recent_sales = processor.time_based_analysis(days=30)
    print(recent_sales.head(10))
    
    # 5. Müşteri harcama seviyeleri
    print("\nMüşteri harcama seviyeleri:")
    spending_levels = processor.customer_spending_analysis()
    spending_counts = spending_levels.value_counts()
    print(spending_counts)
    
    # Görselleştirme
    plt.figure(figsize=(10, 6))
    spending_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Müşteri Harcama Seviyeleri')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()
    
    # 6. Dinamik fiyatlandırma önerileri
    print("\nDinamik fiyatlandırma önerileri:")
    price_updates = processor.dynamic_pricing(threshold=0.2)
    
    # Sadece ilk 10 öneriyi gösterelim
    for i, (product, new_price) in enumerate(price_updates.items()):
        print(f"{product}: {new_price:.2f} TL")
        if i >= 9:
            print(f"... ve {len(price_updates) - 10} ürün daha")
            break
    
    # 7. Ürün önerileri
    print("\nÖrnek müşteri için ürün önerileri (Müşteri ID: 1):")
    recommendations = processor.product_recommendation(customer_id=1)
    print(recommendations)
    
    # 8. Ödeme yöntemi analizi
    print("\nÖdeme yöntemi analizi:")
    payment_analysis = processor.payment_method_analysis()
    print(payment_analysis)
    
    # Görselleştirme
    plt.figure(figsize=(12, 6))
    payment_analysis['İşlem Sayısı'].plot(kind='bar')
    plt.title('Ödeme Yöntemlerine Göre İşlem Sayısı')
    plt.xlabel('Ödeme Yöntemi')
    plt.ylabel('İşlem Sayısı')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # 9. Müşteri demografik analizi
    print("\nMüşteri demografik analizi:")
    demographics = processor.customer_demographics()
    
    if 'Yaş Dağılımı' in demographics:
        print("\nYaş Dağılımı:")
        print(demographics['Yaş Dağılımı'])
    
    if 'Yaş Grupları' in demographics:
        print("\nYaş Grupları:")
        print(demographics['Yaş Grupları'])
        
        # Görselleştirme
        plt.figure(figsize=(10, 6))
        demographics['Yaş Grupları'].plot(kind='bar')
        plt.title('Müşteri Yaş Grupları')
        plt.xlabel('Yaş Grubu')
        plt.ylabel('Müşteri Sayısı')
        plt.tight_layout()
        plt.show()
    
    if 'Cinsiyet Dağılımı' in demographics:
        print("\nCinsiyet Dağılımı:")
        print(demographics['Cinsiyet Dağılımı'])
        
        # Görselleştirme
        plt.figure(figsize=(8, 8))
        demographics['Cinsiyet Dağılımı'].plot(kind='pie', autopct='%1.1f%%')
        plt.title('Müşteri Cinsiyet Dağılımı')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()
    
    # 10. Müşteri memnuniyeti analizi
    print("\nMüşteri memnuniyeti dağılımı:")
    processor.plot_satisfaction_distribution()
    
    # 11. Kategori bazlı satışlar
    print("\nKategori bazlı satışlar:")
    processor.plot_category_sales()
    
    # Sonuçları kaydetme
    print("\nAnaliz sonuçları kaydediliyor...")
    results = {
        'top_products': processor.analyze_top_products(),
        'category_prices': processor.category_price_analysis(),
        'recent_sales': processor.time_based_analysis(days=30),
        'payment_analysis': processor.payment_method_analysis(),
        'missing_data_report': processor.get_missing_data_report(),
        'cleaning_comparison': processor.compare_before_after_cleaning()
    }
    
    # price_updates sözlüğünü DataFrame'e dönüştürme
    price_updates_df = pd.DataFrame(list(price_updates.items()), columns=['Ürün', 'Yeni Fiyat'])
    
    # Excel dosyasına kaydetme
    with pd.ExcelWriter('analiz_sonuclari.xlsx') as writer:
        for sheet_name, data in results.items():
            if isinstance(data, pd.Series):
                data.to_frame().to_excel(writer, sheet_name=sheet_name)
            else:
                data.to_excel(writer, sheet_name=sheet_name)
        
        # price_updates DataFrame'ini ayrıca kaydetme
        price_updates_df.to_excel(writer, sheet_name='price_updates')
    
    print("\nAnaliz tamamlandı! Sonuçlar 'analiz_sonuclari.xlsx' dosyasına kaydedildi.")
    
    if args.use_api:
        print("\nAPI kullanımı hakkında bilgi:")
        print("- API adresi: http://localhost:3000")
        print("- Postman ile aşağıdaki endpoint'lere istek yapabilirsiniz:")
        print("  * Tüm ürünler: GET http://localhost:3000/products")
        print("  * Tek ürün: GET http://localhost:3000/products/1")
        print("  * Ürün filtreleme: GET http://localhost:3000/products?category=Elektronik")
        print("  * Müşteriler: GET http://localhost:3000/customers")
        print("  * Kategoriler: GET http://localhost:3000/categories")

if __name__ == "__main__":
    main() 