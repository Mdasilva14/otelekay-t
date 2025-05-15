# Otel Ziyaretleri — Ziyaretçi Kayıt Sistemi

## Açıklama

**Otel Ziyaretleri**, otellerin ziyaretçi kayıtlarını kolay ve güvenli bir şekilde yönetebilmesi için
**Flask** ile geliştirilmiş bir web uygulamasıdır. Kullanıcı kimlik doğrulama, ziyaretçi CRUD işlemleri
    ve modern Bootstrap tabanlı arayüz ile günlük takibi kolaylaştırır.

## Temel Özellikler

- Kullanıcı kaydı ve yönetimi (giriş/çıkış)
- Ziyaretçiler için tam CRUD işlemleri (oluşturma, okuma, güncelleme, silme)
- Kalıcı veri saklama için SQLite veritabanı
- Yedekleme ve entegrasyon için JSON dosyalarına veri kaydı
- Bootstrap 5 ile duyarlı ve şık kullanıcı arayüzü
- Oturumlar ile erişim kontrolü
- Kolay gezilebilir ve sade tasarım

---

## Kullanılan Teknolojiler

| Teknoloji        | Versiyon | Açıklama                 |
| ---------------- | -------- | ------------------------ |
| Python           | 3.x      | Programlama dili         |
| Flask            | 2.3.2    | Hafif web framework      |
| Flask-SQLAlchemy | Güncel   | Veritabanı ORM           |
| Werkzeug         | Güncel   | Şifreleme ve güvenlik    |
| SQLite           | 3.x      | Gömülü veritabanı        |
| Bootstrap        | 5.3.0    | Duyarlı CSS framework    |
| Jinja2           | Güncel   | Flask için şablon motoru |

## Proje Yapısı

```text
/
├── app.py             # Flask uygulamasının ana dosyası (rota ve iş mantığı)
├── models.py          # SQLAlchemy modelleri (User, Visitor)
├── storage.py         # JSON dosyasına kayıt fonksiyonları (kullanıcı, ziyaretçi)
├── templates/         # Jinja2 HTML şablonları
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── visitors.html
│   └── ...
├── static/            # Statik dosyalar (CSS, JS, resimler)
│   ├── css/
│   ├── js/
│   └── ...
├── users.json         # Kullanıcı verilerini tutan JSON dosyası (opsiyonel)
├── visitors.json      # Ziyaretçi verilerini tutan JSON dosyası (opsiyonel)
└── requirements.txt   # Proje Python bağımlılıkları



