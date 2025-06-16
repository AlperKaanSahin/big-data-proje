import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi oku
df = pd.read_csv("data_yolu")

# Genel ayarlar
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# ---------------------------
#  Rating Dağılımı
# ---------------------------
plt.figure()
sns.histplot(df['Rating'].dropna(), bins=30, kde=True, color="skyblue")
plt.title('Rating Dağılımı')
plt.xlabel('Rating')
plt.ylabel('Frekans')
plt.show()
# ---------------------------
#  Content Rating'e Göre Uygulama Sayısı
# ---------------------------
plt.figure()
sns.countplot(data=df, y='Content Rating', order=df['Content Rating'].value_counts().index, palette='mako')
plt.title('Content Rating Dağılımı')
plt.xlabel('Uygulama Sayısı')
plt.ylabel('Content Rating')
plt.show()

# ---------------------------
#  Ücretli/Mağaza Türüne Göre Uygulama Dağılımı
# ---------------------------
plt.figure()
sns.countplot(data=df, x='Type', palette='Set2')
plt.title('Ücretli ve Ücretsiz Uygulama Dağılımı')
plt.xlabel('Uygulama Türü')
plt.ylabel('Adet')
plt.show()
# ---------------------------
#  Rating & Reviews İlişkisi
# ---------------------------
# Verileri filtrele: sadece 'Everyone' ve 'Free' olanlar
everyone_free_apps = df[(df['Content Rating'] == 'Everyone') & (df['Type'] == 'Free')].copy()

# Reviews sayısını sayıya çevir
everyone_free_apps['Reviews'] = pd.to_numeric(everyone_free_apps['Reviews'], errors='coerce')

# Rating boş olanları çıkar
everyone_free_apps = everyone_free_apps.dropna(subset=['Rating'])

# Grafik
plt.figure(figsize=(10, 6))
sns.scatterplot(data=everyone_free_apps, x='Reviews', y='Rating', alpha=0.5, color='green')
plt.xscale("log")
plt.title('Review Sayısı ve Rating İlişkisi (Everyone & Free)')
plt.xlabel('İnceleme Sayısı (log ölçek)')
plt.ylabel('Puan (Rating)')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# ---------------------------
#  Kategoriye Göre Ortalama Fiyat (sadece ücretli)
# ---------------------------
plt.figure()
paid_apps = df[df['Price'] > 0]
top_paid_cats = paid_apps['Category'].value_counts().head(10).index
sns.barplot(data=paid_apps[paid_apps['Category'].isin(top_paid_cats)],
            y='Category', x='Price', estimator='mean', palette='flare')
plt.title('Kategoriye Göre Ortalama Fiyat (Ücretli Uygulamalar)')
plt.xlabel('Ortalama Fiyat ($)')
plt.ylabel('Kategori')
plt.show()

# ---------------------------

# "Installs" sütununu temizle: virgül ve + işaretlerini kaldır ve int'e çevir
df['Installs'] = df['Installs'].str.replace(',', '').str.replace('+', '').astype(float)

plt.figure(figsize=(10, 6))

free_apps = df[df['Price'] == 0]
top_free_cats = free_apps['Category'].value_counts().head(10).index

# Ortalama indirme sayısına göre sıralama
ordered_cats = free_apps[free_apps['Category'].isin(top_free_cats)].groupby('Category')['Installs'].mean().sort_values(ascending=False).index

sns.barplot(data=free_apps[free_apps['Category'].isin(top_free_cats)],
            y='Category', x='Installs',
            order=ordered_cats,
            estimator='mean', palette='crest')

plt.title('Kategoriye Göre Ortalama İndirme (Ücretsiz Uygulamalar)')
plt.xlabel('Ortalama İndirme Sayısı')
plt.ylabel('Kategori')
plt.xscale("log")
plt.tight_layout()
plt.show()

# ---------------------------
#  Kategoriye Göre Uygulama Sayısı
# ---------------------------
plt.figure(figsize=(10, 12))
cat_counts = df['Category'].value_counts()
sns.barplot(y=cat_counts.index, x=cat_counts.values, palette='pastel')
plt.title('Kategori Bazlı Uygulama Sayısı')
plt.xlabel('Uygulama Sayısı')
plt.ylabel('Kategori')
plt.show()


# Ücretli ve ücretsiz grupları oluştur
df['Price_Type'] = df['Price'].apply(lambda x: 'Ücretli' if x > 0 else 'Ücretsiz')

# En çok uygulamaya sahip ilk 10 kategori
top_categories = df['Category'].value_counts().head(10).index
filtered_df = df[df['Category'].isin(top_categories)]

# Grafik
plt.figure(figsize=(12, 6))
sns.barplot(data=filtered_df,
            x='Category',
            y='Rating',
            hue='Price_Type',
            estimator='mean',
            ci='sd',  # standart sapma ile göster
            palette='Set2')
plt.title('Kategoriye Göre Ortalama Puan (Ücretsiz vs Ücretli)')
plt.xlabel('Kategori')
plt.ylabel('Ortalama Puan')
plt.xticks(rotation=45)
plt.legend(title='Uygulama Tipi')
plt.tight_layout()
plt.show()



plt.figure(figsize=(12, 6))
sns.barplot(data=filtered_df,
            x='Category',
            y='Installs',
            hue='Price_Type',
            estimator='mean',
            ci=None,
            palette='Set1')
plt.yscale("log")  # Büyük farklar varsa log ölçekle göster
plt.title('Kategoriye Göre Ortalama İndirme Sayısı (Ücretsiz vs Ücretli)')
plt.xlabel('Kategori')
plt.ylabel('Ortalama İndirme (Log Ölçek)')
plt.xticks(rotation=45)
plt.legend(title='Uygulama Tipi')
plt.tight_layout()
plt.show()
