
import streamlit as st
from openai import OpenAI
import time
from datetime import datetime, date, time as dt_time
import base64
import json
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ui = {
    "tr": {
        # Giriş Ekranı
        "login_title": "Güvenli Giriş",
        "email_ph": "Okul E-Postası (.edu)",
        "send_code": "Kod Gönder ",
        "enter_code": "Kodu Girin",
        "login_btn": "Giriş Yap 🔓",
        "guest_btn": " Jüri / Misafir Girişi",
        "error_mail": "Lütfen geçerli bir okul maili girin!",
        "success_login": "Giriş Başarılı!",
        "University_email": "Üniversite mailinizi girin.",
        "email_placeholder": "ornek@ogrenci.edu.tr",
        "sunucu_baglantı": "Kod gönderiliyor...",
        "code_sent": "✅ Kod {email} adresine gönderildi! Lütfen kutunuzu (Spam dahil) kontrol et.",
        "kod_gonder": "Doğrulama kodu gönder",
        "school_mail": "Lütfen geçerli bir okul e-postası giriniz.",
        "kodgonder2": "Kod gönderiliyor..",
        "code_sent_msg": "✅ Kod {email} adresine gönderildi! Lütfen kutunuzu (Spam dahil) kontrol edin.",
        "nomail": "Mail gönderilemedi. İnternet bağlantını veya Gmail adresini kontrol et.",
        "nomail2": "Lütfen geçerli bir okul epostası giriniz.",
        "info_code_sent": " Kod **{email}** adresine yollandı.",
        "kodgir": "Lütfen aldığınız 4 haneli kodu girin.",
        "benihatırla": "Beni hatırla",
        "login": "Giriş yap",
        "user": "Kullanıcı",
        "welcome_msg": " Hoş geldin, {user}!",
        "fail": "Hatalı kod!",
        "back": "Geri dön",
        "target": "Hedef Ülke",
        "ai_instr": "Cevapların Türkçe olsun.",
        "countdown": "Kalan Süre",
        "days": "Gün",
        "report_btn": " Raporu İndir (TXT)",
        "report_content": """VISAGUIDE PRO - KİŞİSEL VİZE RAPORU
-----------------------------------
Tarih: {date}
Kullanıcı: {user}

DURUM:
- Randevuya Kalan: {days} Gün

Bu rapor Yapay Zeka destekli VisaGuide Pro tarafından oluşturulmuştur.""",
# --- MVP & VİZYON KISMI ---
        "mvp_title": " **MVP Sürümü (Beta)**",
        "mvp_caption": "Bu proje Microsoft for Startups yarışması için prototip olarak geliştirilmiştir.",
        "roadmap_title": " Gelecek Vizyonu (Roadmap)",
        "roadmap_list": """
        **v2.0 Hedefleri:**
        -  **Kampüs Hayatı:** Okul kulüpleri ve etkinlikleri.
        -  **Mobil Uygulama:** Flutter ile iOS & Android.
        -  **Canlı Sesli Asistan:** Gerçek zamanlı konuşma.
        -  **Canlı Takip:** Uçuş ve vize durumu bildirimleri.
        -  **Tek Tıkla Ödeme:** Sigorta ve harç ödemeleri.
        """,
        "footer_ver": "v1.2.0 • Microsoft for Startups",
        "tabs": [" Süreç", " AI Danışman", " Finans", " Seyahat", " Topluluk", " Acil"],
        "t1_head": "Başvuru Adımları",
        "step": "Adım",
        "completed_tag": "(Tamamlandı)",
        "quick_actions": "⚡ Hızlı İşlemler",
        "doc_analysis_info": " **Belge Analizi**",
        "upload_label": "Belgeyi buraya bırak...",
        "uploaded_caption": "Yüklendi",
        "analyze_btn": " İncele",
        "spinner_analyzing": "AI belgeyi okuyor...",
        "analysis_report_title": "Analiz Raporu:",
        "ai_docs_desc": "Belgelerini AI ile saniyeler içinde oluştur.",
       

       
        # --- ANA BAŞLIK ---
        "app_name": "Nexi",
        "app_tagline": "Yapay zeka destekli profesyonel süreç yönetimi.",
        "btn_intent": " Niyet Mektubu Oluştur",
        "spin_intent": "{country} için taslak yazılıyor...",
        "prompt_intent": "{country} konsolosluğuna hitaben, vize başvurusu için resmi ve profesyonel bir niyet mektubu taslağı yaz. Boşlukları [ ] bırak.",
        "lbl_draft": "Taslak:",
       
        "btn_sponsor": " Sponsor Dilekçesi Yaz",
        "spin_sponsor": "Finansal dilekçe hazırlanıyor...",
        "prompt_sponsor": "{country} vizesi için babanın öğrenciye sponsor olduğuna dair resmi bir dilekçe taslağı yaz. Boşlukları [ ] bırak.",
        "lbl_sponsor_draft": "Sponsorluk Dilekçesi:",
       
        "btn_mail": " Konsolosluk E-Postası",
        "spin_mail": "Mail taslağı çıkarılıyor...",
        "prompt_mail": "{country} konsolosluğuna vize başvurumun durumunu soran çok kibar ve resmi bir e-posta yaz.",
        "lbl_mail_draft": "Mail Taslağı:",
       
        "err_conn": "Bağlantı Hatası",
        "chat_header": "Profesyonel Danışmanı",
        "chat_caption": "{country} resmi prosedürleri ve mevzuatı hakkında sorularınızı yanıtlar.",
        "chat_clear": " Sohbeti Temizle",
        "chat_input_ph": "{country} hakkında bir soru sorun...",
        "conn_error": "Bağlantı Hatası. Lütfen internetinizi kontrol edin.",
       
        # AI'ya gidecek gizli emir (Türkçe)
        "chat_system_prompt": """
        Sen 'Nexi' adında, öğrenciler için tasarlanmış KURUMSAL ve RESMİ bir {country} vize danışmanısın.
       
        KULLANACAĞIN BİLGİ KAYNAĞI: {info}
       
        KURALLAR:
        1. Asla laubali olma. Resmi ve kurumsal dil kullan.
        2. Sadece {country} ile ilgili sorulara cevap ver.
        3. Bilgi bankasındaki verileri kullan, uydurma.
        4. Cevapların Türkçe olsun.
        """,
        "t3_header": "Finans Merkezi",
        "t3_tabs": ["Taşınma Maliyeti", "Aylık Cüzdanım (Takip)"],
        "t3_caption": "{country} macerası için cebinde olması gereken tahmini para.",
        "fixed_costs": "Sabit Giderler",
        "cost_blocked": "• Bloke Hesap: **11.208 €**",
        "cost_visa": "• Vize/Pasaport: **~150 €**",
        "cost_bank": "• Banka Teminatı: **~6.000 €**",
        "cost_equiv": "• Denklik/Vize: **~200 €**",
        "cost_flight": "• Uçak: **~200 €**",
        "variables": "Değişkenler",
        "slider_rent": "İlk Kira (€)",
        "slider_dep": "Depozito (Kira x 2)",
        "slider_gro": "İlk Market Alışverişi (€)",
        "total_start": "Başlangıç Maliyeti",
        "t3_wallet_head": " Giderlerini Kaydet",
        "t3_wallet_caption": "{country} macerandaki aylık harcamalarını not al.",
        "t3_item_label": "Harcama Adı (Örn: Market)",
        "t3_cost_label": "Tutar (€)",
        "add_btn": "➕ Ekle",
        "item_added": "{item} eklendi!",
        "enter_valid": "İsim ve tutar girin.",
        "history_head": " **Harcama Geçmişi**",
        "total_spent": "Toplam Harcanan: {total} €",
        "limit_msg_de": "Aylık bloke hesap limitini (934€) aştın!",
        "limit_msg_it": "Ortalama İtalya öğrenci bütçesini (800€) aştın!",
        "limit_msg_gen": "Bütçe sınırını aştın!",
        "budget_ok": " Bütçe iyi gidiyor: {remaining} € kaldı.",
        "reset_btn": " Listeyi Sıfırla",
        "no_expenses": "Henüz bir harcama eklemedin. Yukarıdan ekleyebilirsin.",
        # --- TAB 4 (SEYAHAT & YAŞAM) İÇİN ---
        "t4_header": "Yaşam ve Konaklama Rehberi",
        "t4_tabs": [" Akıllı Ev Bulucu", " Gezi & Keşif Rotaları"],
       
        # Sekme 1: Ev Bulucu
        "t4_smart_info": " **Kişiliğine Uygun Evi Bul**",
        "t4_smart_cap": "Önce AI sana en uygun semti bulsun, sonra tek tıkla o semtteki ilanlara git.",
        "t4_city_label": "Hangi Şehir?",
        "t4_budget_label": "Max Kira Bütçen (€)",
        "t4_vibe_label": "Nasıl birisin?",
        "t4_vibes_list": ["Gece Hayatı ", "Sessizlik ", "Sanat ", "Doğa ", "Kafe ", "Ucuzluk ", "Güvenlik "],
        "t4_btn_analyze": " Semt Öner ve İlan Getir",
        "t4_warn": "Lütfen en az 2 özellik seç.",
        "t4_spin": "Emlak piyasası taranıyor...",
        "t4_success": "✅ Senin İçin En İyi Bölge: {city}",
        "t4_links_head": " **Bu Kriterlerdeki Gerçek İlanlar:**",
        "t4_search_on": "{site}'da Ara",
        "t4_wait_msg": "Kriterlerini gir, yapay zeka sana semt önersin.",
        # AI Promptları
        "t4_p_sys_home": "Sen {country} emlak uzmanısın. {instr}",
        "t4_p_usr_home": "Şehir: {city}, Bütçe: {budget}€, Tarz: {vibe}. En uygun 1 semti öner, nedenini açıkla ve ortalama kirasını söyle.",
        "t4_trip_info": " **Turist Gibi Değil, Öğrenci Gibi Gez**",
        "t4_trip_city": "Nereyi Gezeceksin?",
        "t4_trip_mode": "Modun Ne?",
        "t4_modes": [" Fotoğraflık", " Ucuz Lezzetler", " Park & Chill", " Müze & Tarih"],
        "t4_btn_route": " Rotamı Oluştur",
        "t4_spin_route": "Rota çiziliyor...",
        "t4_success_route": " {mode} Rotası",
        "t4_map_btn": " Haritada Göster",
        "t4_trip_wait": "Hafta sonu planı için modunu seç.",
        "t5_tabs": [" Yol Arkadaşı", " İkinci El", " Forum"],
        "buddy_find_header": " **Kriterlerine Uygun Arkadaşı Bul**",
        "filter_city_label": "Şehir Filtrele",
        "filter_all": "Tümü",
        "bud_list_header": " **{country} Yolcuları**",
        "filter_all": "Tümü", # Filtre mantığı için gerekli
        "bud_empty_msg": "{city} için henüz kimse kayıt olmamış. İlk sen ol!",
        "bud_connect_btn": "Bağlan",
        "bud_toast_msg": "İletişim Bilgisi: {contact}",
        # AI'ya gidecek komut
        "t4_prompt_trip": "{country}, {city} şehrinde {mode} için turistlerin bilmediği ama öğrencilerin sevdiği 3 gizli yer öner. Çok kısa özetle.",
        "bud_create_title": "Profilini Oluştur",
        "bud_create_desc": "Seninle aynı yere gidenler seni bulsun.",
        "bud_inp_name": "Adın Soyadın",
        "bud_inp_dept": "Bölümün",
        "bud_inp_city": "Gideceğin Şehir",
        "bud_inp_date": "Tahmini Gidiş",
        "bud_inp_interests": "İlgi Alanların (Kafa dengi bulmak için)",
        "bud_interest_opts": ["Gezi ", "Yemek ", "Kodlama ", "Parti ", "Müze ", "Spor ", "Dil Pratiği "],
        "bud_inp_contact": "Instagram / Email",
        "bud_btn_publish": "Profili Yayınla ",
        "bud_success": "Profilin yayında!",
        "market_security_warn": " **Güvenlik:** Ürünü görmeden kapora göndermeyin. Yüz yüze alışverişi tercih edin.",
        "market_showcase_title": " **Vitrin**",
        "market_contact_btn": " Satıcıyla Görüş",
        "market_contact_info": "**Tel/Insta:** {info}",
        "market_whatsapp_btn": "WhatsApp'tan Yaz ",
        "market_save_num": "Numarayı kaydedip arayabilirsin.",
        "market_no_items": "Henüz ilan yok. İlkini sen ekle!",
        "market_sell_title": " **İlan Ver**",
        "market_inp_title": "Ürün Başlığı (Örn: Bisiklet)",
        "market_inp_price": "Fiyat (€)",
        "market_inp_contact": "İletişim (Tel veya Instagram)",
        "market_inp_photo": "Fotoğraf (İsteğe bağlı)",
        "market_btn_publish": "İlanı Yayınla",
        "market_err_contact": "Lütfen iletişim bilgisi giriniz!",
        "market_success": "İlan yayında!",
        "mkt_btn_delete": " Sil",
        "mkt_msg_deleted": "İlan silindi.",
        "mkt_btn_report": " Bildir",
        "mkt_msg_reported": "İlan incelenmek üzere bildirildi.",
        "mkt_empty_list": "Henüz ilan yok. İlkini sen ekle!",

        "mkt_sell_title": " **İlan Ver**",
        "mkt_inp_title": "Ürün Başlığı (Örn: Bisiklet)",
        "mkt_inp_price": "Fiyat (€)",
        "mkt_inp_loc": "Konum",
        "mkt_inp_contact": "İletişim (Tel veya Instagram)",
        "mkt_ph_contact": "Örn: 90555...",
        "mkt_inp_photo": "Fotoğraf (İsteğe bağlı)",
        "mkt_btn_publish": "İlanı Yayınla",
        "mkt_err_contact": "Lütfen iletişim bilgisi giriniz!",
        "mkt_success_msg": "İlan yayında!",
        "sf_new_post_title": " Yeni Gönderi Paylaş",
        "sf_caption_ph": "Ne düşünüyorsun?",
        "sf_photo_label": "Fotoğraf Ekle",
        "sf_btn_share": "Paylaş ",
        "sf_success": "Paylaşıldı!",
        "sf_empty_msg": "Henüz gönderi yok. İlk fotoğrafı sen paylaş!",
        "sf_comments_count": "{count} Yorum",
        "sf_expand_comments": " Yorumları Gör / Yaz",
        "sf_comment_ph": "Yorum ekle...",
        "sf_comment_holder": "Harika görünüyor! ",
        "sf_btn_send": "Gönder",
        "sos_header": "Acil Durum Merkezi",
        "sos_caption": "Panik yapma! Yapay zeka ve hazır kartlar seni yönlendirecek.",
        "sos_advisor_head": " **Durumunu Seç, AI Yönlendirsin**",
        "sos_radio_label": "Ne Oldu?",
        "sos_radio_opts": ["Pasaportumu Kaybettim / Çaldırdım", "Hastalandım / Doktora Gitmem Lazım", "Güvenlik Sorunu / Polislik Durum", "Kalacak Yerim Yok"],
        "sos_help_btn": "YARDIM ET (AI Çözüm)",
        "sos_spinner": "Acil durum protokolü devreye alınıyor...",
        "sos_warning_title": "**YAPMAN GEREKENLER:**",
        "sos_internet_err": "İnternet yok! Yandaki numaraları ara.",
        "sos_numbers_title": "**Önemli Numaralar**",
        "sos_eu_emergency": "Avrupa Genel Acil:",
        "sos_cards_head": "**Hayat Kurtaran Kartlar**",
        "sos_cards_caption": "Polise veya yerel halka göstermek için:",
        "sos_sys_prompt": "Sen {country} ülkesinde bir acil durum asistanısın. Öğrenci şu durumda: {situation}. Ona çok kısa, net ve sakinleştirici 3 adım söyle.",
        "footer_legal": "© 2025 VisaGuide Pro. Microsoft for Startups altyapısıyla geliştirilmiştir. Yasal danışmanlık yerine geçmez.",
        "sos_police": "Polis",
        "sos_ambulance": "Ambulans",
        "sos_consulate": "Konsolosluk",
        "sos_card_doctor_head": "DOKTOR/HASTANE ACİL KART",
        "sos_card_doctor_body": "Şiddetli ağrım var ve acil doktor yardımına ihtiyacım var. Lütfen en yakın hastaneyi gösterin.",
        "sos_card_lost_head": "PASAPORT KAYIP ACİL KART",
        "sos_card_lost_body": "Pasaportumu kaybettim/çaldırdım. Lütfen en yakın polis karakoluna veya Konsolosluğa gitmeme yardım edin.",
        "sos_card_police_head": "ACİL GÜVENLİK / POLİS KART",
        "sos_card_police_body": "Kendimi güvende hissetmiyorum ve hemen polis yardımına ihtiyacım var. Lütfen acil numarayı arayın.",
        "sos_card_stay_head": "ACİL KONAKLAMA KART",
        "sos_card_stay_body": "Bu gece kalacak yerim yok. Lütfen geçici bir öğrenci yurdu veya sığınak bulmama yardım edin.",
        "sos_card_general_ask": "Lütfen bunu çevirmeme yardım edin, yerel dili bilmiyorum.",
        # Yan Menü
        "sidebar_welcome": "Premium Üye",
        "logout": "Çıkış Yap",
       
        # Sekmeler
        "tabs": [" Süreç", " AI Danışman", " Finans", " Seyahat", " Topluluk", " Acil"]
    },
    "en": {
        # Login Screen
        "login_title": "Secure Login",
        "email_ph": "University Email (.edu)",
        "send_code": "Send Code ",
        "enter_code": "Enter Code",
        "login_btn": "Login ",
        "guest_btn": " Jury / Guest Access",
        "error_mail": "Please enter a valid .edu email!",
        "success_login": "Login Successful!",
        "University_email": "University email adress",
        "email_placeholder": "example@student.edu",
        "sunucu_baglantı": "Sending code...",
        "code_sent": "✅ Code sent to {email}! Please check your inbox (including Spam).",
        "kod_gonder": "Send verification code",
        "school_mail": "Please enter a valid school email adress.",
        "kodgonder2": "Sending code..",
        "code_sent_msg": "✅ Code sent to {email}! Please check your inbox (including Spam).",
        "nomail": "Email could not be sent. Check your internet connection or Gmail password.",
        "nomail2": "Please enter a valid school e-mail adress",
        "info_code_sent": " Code sent to **{email}**.",
        "kodgir": "Please enter the 4-digit code you received.",
        "benihatırla": "Remember me",
        "login": "Log in",
        "user": "User",
        "welcome_msg": " Welcome, {user}!",
        "fail": "Wrong code!",
        "back": "Back",
        "target": "Destination",
        "ai_instr": "Answer in English. Be professional.",
        "countdown": "Time Left",
        "days": "Days",
        "report_btn": " Download Report (TXT)",
        "report_content": """VISAGUIDE PRO - PERSONAL STRATEGY REPORT
-----------------------------------
Date: {date}
User: {user}

STATUS:
- Time Left until Appointment: {days} Days

This report was generated by AI-powered VisaGuide Pro.""",
        "mvp_title": " **MVP Version (Beta)**",
        "mvp_caption": "Developed as a prototype for the Microsoft for Startups competition.",
        "roadmap_title": " Future Vision (Roadmap)",
        "roadmap_list": """
        **v2.0 Goals:**
        -  **Campus Life:** School clubs and events.
        -  **Mobile App:** iOS & Android with Flutter.
        -  **Live Voice Assistant:** Real-time conversation.
        -  **Live Tracking:** Flight and visa status notifications.
        -  **One-Click Payment:** Insurance and fee payments.
        """,
        "footer_ver": "v1.2.0 • Microsoft for Startups",
        "tabs": [" Process", " AI Advisor", " Finance", " Travel", " Community", " SOS"],
        "t1_head": "Application Steps", # Başvuru Adımları
        "step": "Step",                 # Adım
        "completed_tag": "(Completed)",
        "quick_actions": " Quick Actions",
        "doc_analysis_info": " **Document Analysis**",
        "upload_label": "Drop file here...",
        "uploaded_caption": "Uploaded",
        "analyze_btn": " Analyze",
        "spinner_analyzing": "AI reading document...",
        "analysis_report_title": "Analysis Report:",
        "ai_docs_desc": "Create your documents with AI in seconds.",
        # AI'ya gidecek resim komutu:
        "vision_prompt": "Is this document suitable for {country} visa application? Analyze dates, type, and validity.",
        "btn_intent": " Motivation Letter",
        "spin_intent": "Drafting for {country}...",
        "prompt_intent": "Write a formal motivation letter for {country} visa application. Leave placeholders as [ ].",
        "lbl_draft": "Draft:",
       
        "btn_sponsor": " Sponsor Letter",
        "spin_sponsor": "Preparing financial letter...",
        "prompt_sponsor": "Write a formal sponsorship letter for {country} visa where the father sponsors the student. Leave placeholders as [ ].",
        "lbl_sponsor_draft": "Sponsorship Draft:",
       
        "btn_mail": " Consulate Email",
        "spin_mail": "Drafting email...",
        "prompt_mail": "Write a very polite and formal email to the {country} consulate inquiring about visa application status.",
        "lbl_mail_draft": "Email Draft:",
       
        "err_conn": "Connection Error",
        "chat_header": "Professional Advisor",
        "chat_caption": "Answers questions about official procedures for {country}.",
        "chat_clear": " Clear Chat",
        "chat_input_ph": "Ask a question about {country}...",
        "conn_error": "Connection Error. Please check your internet.",
        "t5_tabs": [" Find Buddy", " Marketplace", " Forum"],
        "buddy_find_header": " **Find Your Perfect Buddy**",
        "filter_city_label": "Filter by City",
        "filter_all": "All",
        "bud_create_title": "Create Profile",
        "bud_create_desc": "Let others going to the same place find you.",
        "bud_inp_name": "Name Surname",
        "bud_inp_dept": "Department",
        "bud_inp_city": "Target City",
        "bud_inp_date": "Est. Departure",
        "bud_inp_interests": "Interests (To find match)",
        # İlgi alanlarını da çeviriyoruz
        "bud_interest_opts": ["Travel ", "Food ", "Coding ", "Party ", "Museum ", "Sport ", "Language "],
        "bud_inp_contact": "Instagram / Email",
        "bud_btn_publish": "Publish Profile ",
        "bud_success": "Profile Published!",
       
        # AI'ya gidecek gizli emir (İngilizce)
        "chat_system_prompt": """
        You are 'Nexi', a CORPORATE and OFFICIAL visa advisor for {country}.
       
        USE THIS INFO: {info}
       
        RULES:
        1. Never use emojis excessively. Use formal language.
        2. Only answer questions related to {country}.
        3. Use the provided info, do not hallucinate.
        4. Answer in English.
        """,
        "t3_header": "Finance Hub",
        "t3_tabs": ["Startup Cost", "Monthly Wallet"], # Sekme isimleri
        "t3_caption": "Estimated budget needed for your adventure in {country}.",
        "fixed_costs": "Fixed Costs",
        "cost_blocked": "• Blocked Account: **11.208 €**",
        "cost_visa": "• Visa/Passport: **~150 €**",
        "cost_bank": "• Bank Guarantee: **~6.000 €**",
        "cost_equiv": "• Equivalence/Visa: **~200 €**",
        "cost_flight": "• Flight: **~200 €**",
        "variables": "Variables",
        "slider_rent": "First Rent (€)",
        "slider_dep": "Deposit (Rent x 2)",
        "slider_gro": "First Grocery Shop (€)",
        "total_start": "Total Startup Cost",
        "t3_wallet_head": " Record Expenses",
        "t3_wallet_caption": "Track your monthly expenses in {country} here.",
        "t3_item_label": "Expense Name (e.g. Grocery)",
        "t3_cost_label": "Cost (€)",
        "add_btn": " Add",
        "item_added": "{item} added!",
        "enter_valid": "Please enter name and cost.",
        "history_head": " **Expense History**",
        "total_spent": "Total Spent: {total} €",
        "limit_msg_de": "Monthly blocked account limit (934€) exceeded!",
        "limit_msg_it": "Average student budget (800€) exceeded!",
        "limit_msg_gen": "Budget limit exceeded!",
        "budget_ok": " Budget safe: {remaining} € left.",
        "reset_btn": " Reset List",
        "no_expenses": "No expenses yet. Add above.",
        "t4_header": "Travel & Accommodation Guide",
        "t4_tabs": [" Smart Housing", " Explore & Hidden Gems"],
       
        # Sekme 1: Ev Bulucu
        "t4_smart_info": " **Find a Home Matching Your Vibe**",
        "t4_smart_cap": "Let AI suggest the best district, then click to find real listings.",
        "t4_city_label": "Which City?",
        "t4_budget_label": "Max Rent Budget (€)",
        "t4_vibe_label": "What's your vibe?",
        "t4_vibes_list": ["Nightlife ", "Quiet ", "Art ", "Nature ", "Cafe ", "Cheap ", "Safety "],
        "t4_btn_analyze": " Suggest District & Find Ads",
        "t4_warn": "Please select at least 2 traits.",
        "t4_spin": "Scanning real estate market...",
        "t4_success": " Best Match: {city}",
        "t4_links_head": " **Real Listings for Criteria:**",
        "t4_search_on": "Search on {site}",
        "t4_wait_msg": "Enter criteria, let AI suggest districts.",
        # AI Promptları
        "t4_p_sys_home": "You are a real estate expert for {country}. {instr}",
        "t4_p_usr_home": "City: {city}, Budget: {budget}€, Vibe: {vibe}. Suggest 1 best district, explain why, and state avg rent.",
        "t4_trip_info": " **Travel Like a Local**",
        "t4_trip_city": "Where to explore?",
        "t4_trip_mode": "Mode?",
        "t4_modes": [" Photogenic", " Cheap Eats", " Park & Chill", " Museum & History"],
        "t4_btn_route": " Create Route",
        "t4_spin_route": "Planning route...",
        "t4_success_route": " {mode} Route",
        "t4_map_btn": " Show on Map",
        "t4_trip_wait": "Select mode for weekend plan.",
        "bud_list_header": " **{country} Travelers**",
        "filter_all": "All", # Filtre mantığı için gerekli
        "bud_empty_msg": "No one registered for {city} yet. Be the first!",
        "bud_connect_btn": "Connect",

        "bud_toast_msg": "Contact Info: {contact}",
        "bud_list_header": " **{country} Travelers**",
        "filter_all": "All", # Filtre mantığı için gerekli
        "bud_empty_msg": "No one registered for {city} yet. Be the first!",
        "bud_connect_btn": "Connect",
        "bud_toast_msg": "Contact Info: {contact}",
        "market_security_warn": " **Safety:** Prefer face-to-face deals. Do not send money online.",
        "market_showcase_title": " **Showcase**",
        "market_contact_btn": " Contact Seller",
        "market_contact_info": "**Tel/Insta:** {info}",
        "market_whatsapp_btn": "Chat on WhatsApp ",
        "market_save_num": "Save number and call.",
        "market_no_items": "No items yet. Be the first to sell!",
        "market_sell_title": " **Sell Item**",
        "market_inp_title": "Item Title (e.g. Bike)",
        "market_inp_price": "Price (€)",
        "market_inp_contact": "Contact (Tel/Insta)",
        "market_inp_photo": "Photo (Optional)",
        "market_btn_publish": "Publish Ad",
        "market_err_contact": "Contact info is required!",
        "market_success": "Ad Published!",
        "mkt_btn_delete": " Delete",
        "mkt_msg_deleted": "Ad deleted.",
        "mkt_btn_report": " Report",
        "mkt_msg_reported": "Ad reported for review.",
        "mkt_empty_list": "No items yet. Be the first to add!",
        "mkt_sell_title": " **Sell Item**",
        "mkt_inp_title": "Item Title (e.g. Bike)",
        "mkt_inp_price": "Price (€)",
        "mkt_inp_loc": "Location",
        "mkt_inp_contact": "Contact (Phone/Insta)",
        "mkt_ph_contact": "e.g. +90555...",
        "mkt_inp_photo": "Photo (Optional)",
        "mkt_btn_publish": "Publish Ad",
        "mkt_err_contact": "Contact info is required!",
        "mkt_success_msg": "Ad Published!",
        "sf_new_post_title": " New Post",
        "sf_caption_ph": "What's on your mind?",
        "sf_photo_label": "Add Photo",
        "sf_btn_share": "Share ",
        "sf_success": "Posted!",
        "sf_empty_msg": "No posts yet. Be the first to share!",
        "sf_comments_count": "{count} Comments",
        "sf_expand_comments": " View / Write Comments",
        "sf_comment_ph": "Add a comment...",
        "sf_comment_holder": "Looks great! ",
        "sf_btn_send": "Send",
        "sos_header": "Emergency Center",
        "sos_caption": "Don't panic! AI and ready cards will guide you.",
        "sos_advisor_head": " **Select Situation, Let AI Guide You**",
        "sos_radio_label": "What Happened?",
        "sos_radio_opts": ["Passport Lost / Stolen", "Sick / Need Doctor", "Safety Issue / Police Matter", "No Place to Stay"],
        "sos_help_btn": "GET HELP (AI Solution)",
        "sos_spinner": "Activating emergency protocol...",
        "sos_warning_title": "**YOUR NEXT STEPS:**",
        "sos_internet_err": "No internet! Call the numbers next to you.",
        "sos_numbers_title": "**Important Numbers**",
        "sos_eu_emergency": "European General Emergency:",
        "sos_cards_head": "**Life-Saving Cards**",
        "sos_cards_caption": "Show to police or locals:",
        "sos_sys_prompt": "You are a professional emergency assistant for {country}. The student has this situation: {situation}. Provide 3 short, clear, and calming steps.",
        "footer_legal": "© 2025 VisaGuide Pro. Developed with Microsoft for Startups infrastructure. Does not replace legal advice.",
        "sos_police": "Police",
        "sos_ambulance": "Ambulance",
        "sos_consulate": "Consulate",
        "sos_card_doctor_head": "EMERGENCY DOCTOR/HOSPITAL CARD",
        "sos_card_doctor_body": "I have severe pain and need urgent medical assistance. Please show me the nearest hospital.",
        "sos_card_lost_head": "PASSPORT LOST/STOLEN EMERGENCY CARD",
        "sos_card_lost_body": "I have lost/had my passport stolen. Please help me get to the nearest police station or Consulate.",
        "sos_card_police_head": "URGENT SAFETY / POLICE CARD",
        "sos_card_police_body": "I feel unsafe and need police assistance immediately. Please call the emergency number.",
        "sos_card_stay_head": "URGENT ACCOMMODATION CARD",
        "sos_card_stay_body": "I have nowhere to stay tonight. Please help me find a temporary student hostel or shelter.",
        "sos_card_general_ask": "Please help me translate this, I do not speak the local language.",
        # AI'ya gidecek komut
        "t4_prompt_trip": "Suggest 3 hidden gems in {city}, {country} for {mode}. Short summary.",          
        # --- ANA BAŞLIK ---
        "app_name": "Nexi",
        "app_tagline": "AI-powered professional process management.",
    },


        # Sidebar
        "sidebar_welcome": "Premium Member",
        "logout": "Log Out",
       
        # Tabs
        "tabs": [" Process", " AI Advisor", " Finance", " Travel", " Community", " SOS"]
   
}

# --- Dil Seçimini Session State'ten Kontrol Etme ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'tr' 

# 'txt' değişkenini seçilen dile göre atama
txt = ui[st.session_state.lang]

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Nexi", page_icon="⚖️", layout="wide")

# --- TASARIM: FİNAL BLACK & WHITE (MAVİ IŞIK SÖNDÜRÜCÜ) ---
st.markdown("""
<style>
    /* 1. GENEL FONT VE RENKLER */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: #1a1a1a;
    }
    .stApp { background-color: #FFFFFF; }

    /* 2. ANA TEMA RENGİNİ ZORLA DEĞİŞTİRME (KÖKTEN ÇÖZÜM) */
    :root {
        --primary-color: #000000;
        --background-color: #FFFFFF;
        --secondary-background-color: #F0F2F6;
        --text-color: #1a1a1a;
        --font: "DM Sans", sans-serif;
    }

    /* 3. TÜM GİRİŞ KUTULARI (TEXT, NUMBER, DATE, SELECT) */
    /* Normal Halleri */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input, .stSelectbox div[data-baseweb="select"] {
        border: 1px solid #e0e0e0 !important;
        border-radius: 10px !important;
        color: #333 !important;
    }
   
    /* 4. ODAKLANINCA (TIKLAYINCA) ÇIKAN MAVİYİ YOK ETME */
    /* Inputlara tıklayınca kenar SİYAH olsun */
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus, .stDateInput input:focus {
        border-color: #000000 !important;
        box-shadow: 0 0 0 1px #000000 !important; /* Mavi gölge yerine Siyah çizgi */
    }
   
    /* Selectbox (Açılır Liste) tıklanınca */
    div[data-baseweb="select"] > div:focus-within {
        border-color: #000000 !important;
        box-shadow: 0 0 0 1px #000000 !important;
    }

    /* 5. BUTONLAR (SİYAH ZEMİN - BEYAZ YAZI) */
    .stButton > button {
        width: 100%;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #000000 !important;
        border-radius: 12px;
        padding: 14px;
        font-weight: 600 !important;
    }
    .stButton > button p { color: #FFFFFF !important; }
    .stButton > button:hover {
        background-color: #333333 !important;
        border-color: #333333 !important;
        transform: scale(1.01);
    }

    /* 6. DOSYA YÜKLEYİCİ (MAVİ KENARI YOK ET) */
    [data-testid='stFileUploader'] section {
        border: 1px dashed #cccccc !important;
        background-color: #fafafa !important;
    }
    /* Yükleme butonu */
    [data-testid='stFileUploader'] button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: none !important;
    }
   
    /* 2. KAYDIRMA ÇUBUKLARI (SLIDER) - ZARİF TAMİR */
    /* Çubuğun arka planı (Boş kısım) - Açık Gri */
    div[data-baseweb="slider"] > div:first-child {
        background-color: #FFFFFF !important;
    }
    /* Çubuğun dolu kısmı - Siyah */
    div[data-baseweb="slider"] div[data-testid="stTickBar"] {
        background-color: #000000 !important;
    }
    /* Yuvarlak tutamaç (Top) - Siyah */
    div[role="slider"] {
        background-color: #000000 !important;
        border-color: #000000 !important;
        box-shadow: none !important; /* Etrafındaki gölgeyi kaldır */
    }
    /* Tıklayınca (Focus) etrafında çıkan ışığı siyah yap */
    div[role="slider"]:focus-visible {
        box-shadow: 0 0 0 2px #000000 !important;
    }

    /* 8. CHECKBOX VE RADYO (SİYAH TİK) */
    .stCheckbox > label > div[role="checkbox"][aria-checked="true"] {
        background-color: #000000 !important;
        border-color: #000000 !important;
    }
    div[role="radiogroup"] > label > div:first-child {
        background-color: #000000 !important;
        border-color: #000000 !important;
    }

    /* 9. SEKME (TAB) SEÇİM RENGİ */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [aria-selected="true"] {
        color: #000000 !important;
        border-bottom-color: #000000 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #000000 !important;
    }

    /* 10. BİLGİ KUTULARI (BEYAZ) */
    div[data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        border: 1px solid #EAEAEA !important;
        color: #333333 !important;
        border-radius: 12px;
    }
    div[data-testid="stAlert"] * { color: #333333 !important; }
   
    /* 11. LINKLER */
    a { color: #000000 !important; text-decoration: underline; }

</style>
""", unsafe_allow_html=True)

# --- API ANAHTARI ---
# Şifreyi koddan değil, sunucunun gizli kasasından çekiyoruz
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)
# --- GERÇEK MAİL GÖNDERME FONKSİYONU ---
def mail_gonder(alici_mail, kod):
    sender_email = "oykud8826@gmail.com"  # Örn: ahmet@gmail.com
    sender_password = "ofdrgkqnppyhlzqz " # Boşluksuz yaz
   
    subject = "Nexi - Doğrulama Kodunuz"
    body = f"""
    Merhaba,
   
    Nexi öğrenci topluluğuna hoş geldiniz! Bizi bu yolculuğa dahil ettiğiniz çok teşekkürler!
   
    Giriş Kodunuz: {kod}
   
    Bu kodu kimseyle paylaşmayın.
    Başarılar!
    """
   
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = alici_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
   
    try:
        # Gmail Sunucusuna Bağlan (Port 587)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Güvenli bağlantı
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, alici_mail, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Mail Hatası: {e}")
        return False

# --- GİRİŞ EKRANI SİMÜLASYONU ---
if "kullanici_adi" not in st.session_state:
    st.session_state.kullanici_adi = "Ziyaretçi"
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False
   

   
    # --- GİRİŞ EKRANI (GERÇEK MAİL GÖNDERMELİ) ---
if not st.session_state.giris_yapildi:
    col_log1, col_log2, col_log3 = st.columns([1, 2, 1])
    with col_log2:
        # 1. DİL SEÇİMİ (EN ÜSTTE)
        dil_secimi = st.radio("Dil / Language", ["Türkçe", "English"], horizontal=True)
        # Seçime göre dili ayarla
        lang = "tr" if dil_secimi == "Türkçe" else "en"
        st.session_state.lang = lang # Kaydet
        txt = ui[lang] # Sözlükten kelimeleri çek
        st.markdown("""
        <div style="background-color: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; border: 1px solid #eee;">
            <h1 style="color: #000; margin-bottom: 10px;">Nexi</h1>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
   
   

   
       
        # AŞAMA 1: MAİL GİRİŞİ
        if not st.session_state.get("dogrulama_asamasinda"):
            mail_input = st.text_input(txt["University_email"], placeholder=txt["email_placeholder"])
           
            if st.button(txt["kod_gonder"], use_container_width=True):
                if "edu" in mail_input or "student" in mail_input:
                    uretilen_kod = str(random.randint(1000, 9999))
                   
                    # --- GERÇEK MAİL GÖNDERME İŞLEMİ ---
                    with st.spinner(txt["sunucu_baglantı"]):
                        try:
                            # Yukarıda tanımladığımız fonksiyonu çağırıyoruz
                            basari = mail_gonder(mail_input, uretilen_kod)
                        except NameError:
                            st.error("Hata: mail_gonder fonksiyonu bulunamadı! Kodun en tepesine eklemeyi unuttun mu?")
                            basari = False
                        except Exception as e:
                            st.error(f"Beklenmedik hata: {e}")
                            basari = False

                    if basari:
                        # Mail gittiyse hafızaya al
                        st.session_state.dogrulama_kodu = uretilen_kod
                        st.session_state.girilen_mail = mail_input
                        st.session_state.dogrulama_asamasinda = True
                        st.success(txt['code_sent'].format(email=mail_input))
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Mail gönderilemedi. Gmail 'Uygulama Şifresi'ni doğru girdin mi?")
                    # -----------------------------------
                else:
                    st.error(txt["school_mail"])
                   
                    # --- GERÇEK MAİL GÖNDERME ---
                    with st.spinner(txt["kodgonder2"]):
                        try:
                            # Yukarıdaki mail_gonder fonksiyonunu çağırıyoruz
                            basari = mail_gonder(mail_input, uretilen_kod)
                        except NameError:
                            st.error("Hata: mail_gonder fonksiyonu bulunamadı! Kodun tepesine ekledin mi?")
                            basari = False

                    if basari:
                        st.session_state.dogrulama_kodu = uretilen_kod
                        st.session_state.girilen_mail = mail_input
                        st.session_state.dogrulama_asamasinda = True
                        st.success(txt['code_sent_msg'].format(email=mail_input))
                        st.rerun()
                    else:
                        st.error(txt["nomail"])
               
            else:
                    st.error(txt["nomail2"])
               

        # AŞAMA 2: KOD DOĞRULAMA
        else:
            st.info(txt['info_code_sent'].format(email=st.session_state.girilen_mail))
            # (Test ederken mail beklemek istemezsen bu satırı açabilirsin)
            #print(f"GİZLİ KOD: {st.session_state.dogrulama_kodu}")

            girilen_kod = st.text_input(txt["kodgir"], max_chars=4, placeholder="XXXX")
            beni_hatirla = st.checkbox(txt["benihatırla"])
           
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button(txt["login"], use_container_width=True):
                    if girilen_kod == st.session_state.dogrulama_kodu:
                        st.session_state.giris_yapildi = True
                        # İsim alma (Mailden çıkarma)
                        st.session_state.kullanici_adi = st.session_state.girilen_mail.split("@")[0].capitalize()
                       
                        if beni_hatirla:
                            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                                json.dump({txt["user"]: st.session_state.kullanici_adi}, f)
                       
                        st.balloons()
                        st.success(txt['welcome_msg'].format(user=st.session_state.kullanici_adi))
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(txt["fail"])
            with col_b2:
                if st.button(txt["back"], use_container_width=True):
                    st.session_state.dogrulama_asamasinda = False
                    st.rerun()
    st.stop() # Giriş yoksa dur
# --- BİLGİ BANKASI ---
# --- AKILLI VERİ TABANI (DETAYLANDIRILMIŞ VERSİYON) ---
# --- 5. VERİTABANI (ÇİFT DİLLİ - TAM DETAYLI) ---
country_data = {
    " Germany": {
        # --- İNGİLİZCE İÇERİK ---
        "check_en": [
            "Passport (Valid min 1 year + 2 copies)",
            "Admission Letter (Zulassungsbescheid)",
            "Blocked Account Proof (11.208€)",
            "Motivation Letter (Signed)",
            "Travel Health Insurance (Incoming)",
            "Biometric Photo (3 Pcs)"
        ],
        "info_en": """
        GERMANY STUDENT VISA (TYPE D) & LIFE DETAILS:

        1. FINANCIAL PROOF (BLOCKED ACCOUNT):
           - 2024/2025 requirement: 11,208 Euro/year (Net).
           - Monthly withdrawal limit: 934 Euro.
           - Providers: Fintiba, Expatrio, Coracle (All digital).
           - Alternative: 'Letter of Commitment' (Verpflichtungserklärung) from a resident.

        2. DOCUMENTS & PROCESS:
           - Visa Fee: 75 Euro (Cash) + iDATA Service Fee (~33 Euro).
           - Health Insurance: 'Incoming' travel insurance (min 30k€) for visa. 'Public Insurance' (TK, AOK) for university enrollment.
           - Waiting Time: 4-8 weeks via iDATA appointment.

        3. ARRIVAL (FIRST STEPS):
           - Anmeldung (Registration): Must register address at Bürgeramt within 14 days.
           - Radio Tax (Rundfunkbeitrag): Every household pays 18.36 Euro/month.
           - Sim Card: Aldi Talk or Vodafone prepaid are common.

        4. WORK & LIFE:
           - Work Permit: 120 full days or 240 half days per year.
           - Min Wage: Approx. 12.41 Euro/hour.
        """,

        # --- TÜRKÇE İÇERİK (SENİN METİNLERİN) ---
        "check_tr": [
            "Pasaport (En az 1 yıl geçerli + 2 fotokopi)",
            "Okul Kabul Belgesi (Zulassungsbescheid)",
            "Bloke Hesap Onayı (11.208€)",
            "Motivasyon Mektubu (İmzalı)",
            "Seyahat Sağlık Sigortası (Incoming)",
            "Biometrik Fotoğraf (3 Adet)"
        ],
        "info_tr": """
        ALMANYA ÖĞRENCİ VİZESİ (D TİPİ) VE YAŞAM DETAYLARI:
       
        1. FİNANSAL KANIT (BLOKE HESAP):
           - 2024/2025 dönemi için yıllık net teminat: 11.208 Euro.
           - Aylık çekim hakkı: 934 Euro.
           - Sağlayıcılar: Fintiba, Expatrio, Coracle (Hepsi dijitaldir).
           - Alternatif: Almanya'da yaşayan birinin 'Garantör Belgesi' (Verpflichtungserklärung) vermesi.

        2. BELGELER VE SÜREÇ:
           - Vize Harcı: 75 Euro (Euro nakit) + iDATA Hizmet Bedeli (~33 Euro TL).
           - Sağlık Sigortası: Vize için 'Incoming' seyahat sigortası (min. 30.000€ teminat). Okula kayıt için 'Kamu Sigortası' (TK, AOK) gerekir.
           - Bekleme Süresi: iDATA üzerinden randevu ataması 4-8 hafta sürebilir.

        3. ALMANYA'YA VARIŞ (İLK İŞLER):
           - Anmeldung (İkamet Kaydı): İndikten sonra 14 gün içinde Bürgeramt'a gidip adres beyanı yapılmalıdır.
           - Rundfunkbeitrag: Her hane aylık 18.36 Euro Radyo/TV vergisi öder.
           - Sim Kart: Aldi Talk veya Vodafone ön ödemeli hatlar yaygındır.

        4. ÇALIŞMA VE YAŞAM:
           - Çalışma İzni: Yılda 120 tam gün veya 240 yarım gün.
           - Asgari Ücret: Saatlik yaklaşık 12.41 Euro.
        """,
        "cost": 11500, 
        "cities": ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt", "Stuttgart"] ,
        
        'info': ""
    },
   
    " Italy": {
        "check_en": [
            "Universitaly Summary (Approved)",
            "Grant Letter or Bank Statement (Min 6000€)",
            "Accommodation Proof",
            "Flight Reservation",
            "DOV or CIMEA Declaration",
            "Passport and Photos"
        ],
        "info_en": """
        ITALY STUDENT VISA & ERASMUS DETAILS:

        1. UNIVERSITY PRE-ENROLLMENT (CRITICAL):
           - UNIVERSITALY: Mandatory portal for all applications. No visa without this approval.
           - DOV (Declaration of Value): Diploma equivalence from the Consulate.
           - CIMEA: Digital alternative to DOV (Faster but paid).

        2. FINANCIAL STATUS:
           - NO Blocked Account required.
           - Bank Statement: Must show annual living costs (Approx. 6000-8000 Euro).
           - Grant: Erasmus grant letter is accepted as proof.

        3. ARRIVAL (FIRST STEPS):
           - Codice Fiscale: Italian Tax ID. Mandatory for rent, sim card, bank.
           - Permesso di Soggiorno: Residence Permit. Must apply at a post office (Kit Giallo) within 8 DAYS of arrival.

        4. SCHOLARSHIP & LIFE:
           - DSU Scholarship: Regional aid based on family income (ISEE). Covers dorm/meals.
           - Rent: North (Milan) is expensive, South (Naples) is cheaper.
        """,
        "check_tr": [
            "Universitaly Ön Kayıt Özeti (Onaylı)",
            "Hibe Yazısı veya Banka Dökümü (Min 6000€)",
            "Konaklama Belgesi (Yurt/Kira Kontratı)",
            "Uçak Rezervasyonu",
            "DOV veya CIMEA Denklik Belgesi",
            "Pasaport ve Fotoğraflar"
        ],
        "info_tr": """
        İTALYA ÖĞRENCİ VİZESİ VE ERASMUS DETAYLARI:

        1. ÜNİVERSİTE ÖN KAYIT (ÇOK ÖNEMLİ):
           - UNIVERSITALY: İtalya'daki tüm başvurular 'Universitaly.it' portalı üzerinden yapılır. Bu onay olmadan vizeye başvurulamaz.
           - DOV (Dichiarazione di Valore): Diploma Denklik Belgesi. Konsolosluk eğitim ataşeliğinden alınır.
           - CIMEA: DOV yerine geçen dijital denklik belgesidir (Daha hızlıdır ama paralıdır).

        2. FİNANSAL DURUM:
           - Bloke Hesap YOKTUR.
           - Banka Dökümü: Kendi veya sponsorunun hesabında yıllık yaşam masrafını (Yaklaşık 6.000 - 8.000 Euro) gösteren banka dökümü gerekir.
           - Hibe: Erasmus hibesi alıyorsan, hibe yazısı finansal kanıt yerine geçer.

        3. İTALYA'YA VARIŞ (İLK İŞLER):
           - Codice Fiscale: İtalyan Vergi Numarası. Ev kiralamak, hat almak, banka açmak için ŞARTTIR. Konsolosluktan veya İtalya'da vergi dairesinden (Agenzia delle Entrate) alınır.
           - Permesso di Soggiorno: Oturum izni. İtalya'ya indikten sonra 8 GÜN İÇİNDE postaneden (Kit Giallo) başvuru yapılmalıdır.

        4. BURS VE YAŞAM:
           - DSU Bursu: Ailenin gelir durumuna (ISEE) göre verilen bölgesel burstur. Yurt ve yemekhane imkanı sağlar.
           - Kira: Kuzey İtalya (Milano) çok pahalıdır, Güney (Napoli) daha uygundur.
        """,
        "cost": 6500, "cities": ["Rome", "Milan", "Turin", "Bologna", "Naples", "Florence"],
        'info': ""
    },

    " Poland": {
        "check_en": ["Passport", "Grant Letter", "Admission Letter", "Travel Insurance (30k€)", "Flight Reservation"],
        "info_en": """
        POLAND VISA (TYPE D) DETAILS:
        1. PROCESS: Apply via VFS Global. Appointments are hard to find (Check at 08:00 AM).
        2. FINANCE: Cheapest option. Grant usually covers costs. Or show ~2500 PLN + Monthly 776 PLN.
        3. ARRIVAL: PESEL Number (ID) is given after address registration (Zameldowanie).
        4. DORMS: State dorms are very cheap (100-150 Euro).
        """,
        "check_tr": ["Pasaport", "Erasmus Hibe Yazısı", "Okul Kabul Mektubu", "Seyahat Sigortası (30.000€)", "Uçak Rezervasyonu"],
        "info_tr": """
        POLONYA VİZESİ (D TİPİ) VE YAŞAM DETAYLARI:
        1. VİZE SÜRECİ (VFS GLOBAL):
           - Başvuru: VFS Global aracı kurumu üzerinden yapılır. Randevu bulmak zordur, sabah 08:00-09:00 arası sistem kontrol edilmelidir.
           - Vize Ücreti: Türk öğrencilere vize harcı genelde yoktur, sadece VFS hizmet bedeli ödenir.
        2. FİNANSAL KANIT (EN UCUZ ÜLKE):
           - Tutar: Dönüş bileti parası (yaklaşık 2500 PLN) + Aylık yaşam masrafı (776 PLN x Kalınacak Ay) hesapta gösterilmelidir.
           - Hibe: Erasmus hibesi Polonya için genelde tek başına yeterlidir.
        3. VARIŞ VE BÜROKRASİ:
           - PESEL Numarası: Polonya'nın TC kimlik numarasıdır. İkamet kaydı (Zameldowanie) yapınca verilir.
           - Yurtlar: Devlet yurtları (Dom Studencki) aylık 100-150 Euro gibi komik rakamlara bulunabilir.
        """,
        "cost": 3500, "cities": ["Warsaw", "Krakow", "Lodz", "Wroclaw", "Poznan", "Gdansk"],
        'info': ""
    },

    " Spain": {
        "check_en": ["Passport", "Medical Report", "Criminal Record (Apostille)", "Grant Letter", "Admission Letter"],
        "info_en": """
        SPAIN VISA DETAILS:
        1. CRITICAL DOCS: Medical Certificate (Intl. Health Regulations 2005) is MANDATORY. Criminal Record must have Apostille.
        2. APPLICATION: Via BLS International.
        3. FINANCE: IPREM Index (600 Euro/Month).
        4. ARRIVAL: Empadronamiento (Address registration) and TIE Card (Residency for >6 months).
        """,
        "check_tr": ["Pasaport", "Sağlık Heyet Raporu", "Adli Sicil Kaydı (Apostilli)", "Hibe/Banka Dökümü", "Okul Kabulü"],
        "info_tr": """
        İSPANYA VİZESİ VE YAŞAM DETAYLARI:
        1. KRİTİK BELGELER (ZORLU SÜREÇ):
           - Sağlık Heyet Raporu: "2005 Uluslararası Sağlık Tüzüğü'ne göre bulaşıcı hastalık taşımamaktadır" ibaresi içeren, apostilli ve İspanyolca tercümeli heyet raporu ŞARTTIR.
           - Adli Sicil Kaydı: E-devletten alınır, Lahey Apostili yapılması ve tercüme edilmesi zorunludur.
           - Başvuru Merkezi: BLS International.
        2. FİNANSAL DURUM:
           - IPREM Endeksi: İspanya asgari yaşam endeksidir (Aylık 600 Euro).
        3. İSPANYA'YA VARIŞ:
           - Empadronamiento: Belediye binasına gidip adres kaydı yaptırma işlemidir.
           - TIE Kartı (Oturum): Eğer vizeniz 6 aydan uzunsa, ilk 1 ay içinde polise gidip parmak izi vererek TIE almanız gerekir.
        """,
        "cost": 5000, "cities": ["Madrid", "Barcelona", "Valencia", "Seville", "Granada", "Bilbao"],
        'info': ""
    },

    " France": {
        "check_en": ["Passport", "Campus France Approval", "Etudes en France No", "Bank Statement", "Accommodation Proof"],
        "info_en": """
        FRANCE VISA (VLS-TS) DETAILS:
        1. CAMPUS FRANCE: Mandatory first step. Interview required. 'Etudes en France' portal is used.
        2. FINANCE: Min 615 Euro/month. No blocked account.
        3. BENEFITS: CAF (Housing Aid) is available for all students (30-40% of rent returned).
        4. ARRIVAL: Must validate visa online (OFII) and pay tax.
        """,
        "check_tr": ["Pasaport", "Campus France Onayı", "Etudes en France No", "Banka Dökümü (Min 615€/Ay)", "Konaklama Belgesi"],
        "info_tr": """
        FRANSA VİZESİ (VLS-TS) VE YAŞAM:
        1. CAMPUS FRANCE (ZORUNLU İLK ADIM):
           - Vizeden önce "Campus France Türkiye" üzerinden dosya açılmalı ve mülakata girilmelidir. Campus France onayı olmadan vize alınamaz.
        2. VİZE VE FİNANS:
           - Vize Türü: VLS-TS (Oturum izni yerine geçen uzun süreli vize).
           - Maddi Kanıt: Aylık en az 615 Euro kaynak gösterilmelidir.
        3. AVANTAJLAR (KİRA YARDIMI):
           - CAF (Kira Yardımı): Fransa'da devlet, yabancı öğrenciler dahil herkese kira yardımı (APL) yapar.
           - CVEC: Öğrenci hayatı katkı payı (Yıllık ~100 Euro).
        """,
        "cost": 7000, "cities": ["Paris", "Lyon", "Toulouse", "Bordeaux", "Marseille", "Lille"],
        'info': ""
    }
}


   
# --- YAN MENÜ (Kısa ve Öz) ---
# --- YAN MENÜ (SIDEBAR) - GÜNCELLENMİŞ HALİ ---
with st.sidebar:
    # 1. PROFİL KARTI (DİNAMİK - GİRİŞ YAPAN İSMİ GÖSTERİR)
    aktif_kullanici = st.session_state.kullanici_adi  # Giriş ekranından gelen isim
   
    st.markdown(f"""
    <div style="background-color: #F2E8E8; padding: 15px; border-radius: 10px; margin-bottom: 20px; border;">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 30px; margin-right: 10px;">🎓</div>
            <div>
                <div style="font-weight: bold; color: #1E3A8A;">{aktif_kullanici}</div>
                <div style="font-size: 12px; color: #666;</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # --- ÜLKE SEÇİMİ (DİL DESTEKLİ) ---
    # "Hedef Ülke" yerine txt['target'] kullandık
    secilen_ulke = st.selectbox(txt['target'], list(country_data.keys()))
    aktif_veri = country_data[secilen_ulke]

    # --- CHAT HAFIZASINI SIFIRLAMA ---
    if "son_secilen_ulke" not in st.session_state:
        st.session_state.son_secilen_ulke = secilen_ulke
       
    if st.session_state.son_secilen_ulke != secilen_ulke:
        # AI Beynini de dile göre güncelliyoruz!
        # txt['ai_instr'] -> "Answer in English" veya "Türkçe cevapla" emrini içerir
        st.session_state.messages = [{
            "role": "system",
            "content": f"Sen {secilen_ulke} uzmanısın. BİLGİLER: {aktif_veri['info']}. {txt['ai_instr']}"
        }]
        st.session_state.son_secilen_ulke = secilen_ulke
        st.rerun()

    st.divider()

    hedef_tarih = st.date_input("Date", value=date(2026, 1, 15))
    simdi = datetime.now()
    hedef_zaman = datetime.combine(hedef_tarih, dt_time(9, 0))
    fark = hedef_zaman - simdi
   
    if fark.total_seconds() > 0:
        # Sözlükten çekiyoruz: "Kalan Süre" veya "Time Left"
        st.metric(txt['countdown'], f"{fark.days} {txt['days']}", delta="⏳")
        st.progress(max(0, min(100, 100 - fark.days)))
   
    st.divider()
   
    # --- 4. RAPOR İNDİRME BUTONU (DİNAMİK) ---
    aktif_kullanici = st.session_state.get("kullanici_adi", "Misafir")

    # BURASI SİHİRLİ KISIM:
    # 1. txt['report_content'] ile dile göre şablonu çekiyor.
    # 2. .format(...) ile boşlukları dolduruyor.
    rapor_icerigi = txt['report_content'].format(
        date=datetime.now().strftime("%d.%m.%Y"),
        user=aktif_kullanici,
        days=fark.days
    )
   
    st.download_button(
        label=txt['report_btn'], # Buton üzerindeki yazı
        data=rapor_icerigi,      # Dosyanın içindeki yazı
        file_name="visaguide_report.txt",
        mime="text/plain",
    )
    # --- MVP & VİZYON KUTUSU (ÇİFT DİLLİ) ---
    st.info(txt['mvp_title'])
    st.caption(txt['mvp_caption'])
   
    with st.expander(txt['roadmap_title']):
        st.markdown(txt['roadmap_list'])
   
    st.divider()
   
    st.caption(txt['footer_ver'])

# --- ANA BAŞLIK (ÇİFT DİLLİ) ---
st.title(txt['app_name'])
st.markdown(f"""
<p style="font-size: 20px; color: #555; margin-top: -15px;">
    {txt['app_tagline']}
</p>
<hr style="margin-top: 0; margin-bottom: 30px; border: 0; border-top: 1px solid #eee;">
""", unsafe_allow_html=True)

# --- SEKMELER (DİL DESTEKLİ) ---
# Sekme isimlerini sözlükten çekiyoruz
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(txt['tabs'])

with tab1:
    c1, c2 = st.columns([1.5, 1], gap="large")
   
    # --- SOL SÜTUN (ÇİFT DİLLİ) ---
    with c1:
        # Başlık: "{secilen_ulke} Application Steps"
        st.subheader(f"📌 {secilen_ulke} {txt['t1_head']}")
       
        # Dile göre doğru checklist listesini seçiyoruz (check_en veya check_tr)
        checklist_key = "check_en" if st.session_state.lang == "en" else "check_tr"
       
        # Döngü
        for i, madde in enumerate(aktif_veri[checklist_key], 1):
            key_val = f"task_{secilen_ulke}_{i}"
           
            # "Adım 1" veya "Step 1" yazısı
            with st.expander(f"{txt['step']} {i}", expanded=(i==1)):
                c_kutu, c_yazi = st.columns([0.1, 0.9])
               
                with c_kutu:
                    durum = st.checkbox("", key=key_val)
               
                with c_yazi:
                    if durum:
                        # Üstü çizili ve "(Completed)" yazısı
                        st.markdown(f"""
                        <div style="text-decoration: line-through; color: #999; margin-top: 5px;">
                            {madde} <span style="font-size:12px;">{txt['completed_tag']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="color: #333; font-weight: 600; margin-top: 5px;">
                            {madde}
                        </div>
                        """, unsafe_allow_html=True)

    # --- SAĞ SÜTUN: BELGE TARAYICI VE 3 SİHİRLİ BUTON ---
    with c2:
        st.subheader(txt['quick_actions']) # "Hızlı İşlemler"
        st.info(txt['doc_analysis_info'])  # "Belge Analizi"
       
        # 1. BELGE TARAYICI (VISION)
        uploaded_file = st.file_uploader(txt['upload_label'], type=["jpg", "png", "jpeg"])
       
        if uploaded_file:
            st.image(uploaded_file, caption=txt['uploaded_caption'], use_container_width=True)
           
            if st.button(txt['analyze_btn']): # "İncele" Butonu
                with st.spinner(txt['spinner_analyzing']):
                    try:
                        b64 = encode_image(uploaded_file)
                       
                        # AI Komutunu dilden çekiyoruz ve içine ülkeyi koyuyoruz
                        prompt_text = txt['vision_prompt'].format(country=secilen_ulke)
                       
                        res = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt_text},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                                ]
                            }]
                        )
                        st.success(txt['analysis_report_title'])
                        st.write(res.choices[0].message.content)
                    except Exception as e: st.error(f"Error: {e}")
       
        st.divider()
        st.write(txt['ai_docs_desc']) # "Belgelerini AI ile oluştur..."
       
       

        # 2. BUTON: NİYET MEKTUBU (DİNAMİK & ÇİFT DİLLİ)
        if st.button(txt['btn_intent']):
            with st.spinner(txt['spin_intent'].format(country=secilen_ulke)):
                try:
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": txt['prompt_intent'].format(country=secilen_ulke)}]
                    )
                    st.text_area(txt['lbl_draft'], value=res.choices[0].message.content, height=200)
                except: st.error(txt['err_conn'])

        # 3. BUTON: SPONSORLUK DİLEKÇESİ (DİNAMİK & ÇİFT DİLLİ)
        if st.button(txt['btn_sponsor']):
            with st.spinner(txt['spin_sponsor']):
                try:
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": txt['prompt_sponsor'].format(country=secilen_ulke)}]
                    )
                    st.text_area(txt['lbl_sponsor_draft'], value=res.choices[0].message.content, height=200)
                except: st.error(txt['err_conn'])

        # 4. BUTON: RESMİ MAİL (DİNAMİK & ÇİFT DİLLİ)
        if st.button(txt['btn_mail']):
            with st.spinner(txt['spin_mail']):
                try:
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": txt['prompt_mail'].format(country=secilen_ulke)}]
                    )
                    st.text_area(txt['lbl_mail_draft'], value=res.choices[0].message.content, height=200)
                except: st.error(txt['err_conn'])
# --- TAB 2: AI CHAT (DİNAMİK & ÇİFT DİLLİ) ---
with tab2:
    # Başlık ve Açıklama (Sözlükten doluyor)
    st.subheader(f"💬 {secilen_ulke} {txt['chat_header']}")
    st.caption(txt['chat_caption'].format(country=secilen_ulke))
   
    # Sohbeti Temizle Butonu
    if st.button(txt['chat_clear']):
        st.session_state.messages = []
        st.rerun()

    # --- AI BEYNİ (DİNAMİK PROMPT) ---
    # Eğer hafıza boşsa, seçilen dilin promptuyla başlat
    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        # Prompt metnini sözlükten çekip içini dolduruyoruz
        system_msg = txt['chat_system_prompt'].format(
            country=secilen_ulke,
            info=aktif_veri['info']
        )
        st.session_state.messages = [{"role": "system", "content": system_msg}]

    # Mesajları Göster
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Soru Sorma Kısmı
    if prompt := st.chat_input(txt['chat_input_ph'].format(country=secilen_ulke)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages
                )
                full_response = response.choices[0].message.content
                message_placeholder.write(full_response)
                # Cevabı hafızaya kaydet
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(txt['conn_error'])
# --- TAB 3: FİNANS MERKEZİ (DİNAMİK & ÇİFT DİLLİ) ---
with tab3:
    st.header(f"{secilen_ulke} {txt['t3_header']}")
   
    # Sekme isimlerini sözlükten (listeden) çekiyoruz
    butce_tab1, butce_tab2 = st.tabs(txt['t3_tabs'])

    # --- ALT SEKME 1: TAŞINMA MALİYETİ ---
    with butce_tab1:
        # Caption içindeki {country} kısmını dolduruyoruz
        st.caption(txt['t3_caption'].format(country=secilen_ulke))
       
        col_b1, col_b2 = st.columns([1, 1], gap="large")
        with col_b1:
            st.info(f"**{txt['fixed_costs']}**")
           
            # Ülkeye göre verileri değiştiriyoruz
            if "Almanya" in secilen_ulke:
                st.write(txt['cost_blocked'])
                st.write(txt['cost_visa'])
                sabit_tutar = 11208 + 150
            else: # İtalya ise
                st.write(txt['cost_bank'])
                st.write(txt['cost_equiv'])
                sabit_tutar = 6000 + 200
               
            st.write(txt['cost_flight'])
            fixed = sabit_tutar + 200
           
        with col_b2:
            st.warning(f"**{txt['variables']}**")
            kira = st.slider(txt['slider_rent'], 300, 1500, 600)
            depozito = st.slider(txt['slider_dep'], 600, 3000, 1200)
            market = st.slider(txt['slider_gro'], 100, 500, 200)
            variable = kira + depozito + market
       
        st.divider()
        toplam_start = fixed + variable
        st.metric(txt['total_start'], f"{toplam_start} €")

    # --- ALT SEKME 2: AYLIK HARCAMA TAKİBİ (AYNI KALDI, SADECE LİMİT DİNAMİK) ---
    with butce_tab2:
        st.subheader(" Giderlerini Kaydet")
        st.caption(f"{secilen_ulke}'daki aylık harcamalarını buraya not al.")

        # Hafıza (Session State)
        if "harcamalar" not in st.session_state:
            st.session_state.harcamalar = []

        # 1. VERİ GİRİŞ ALANI
        with st.container():
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                kalem = st.text_input("Harcama Adı (Örn: Market)", key="h_ad")
            with c2:
                tutar = st.number_input("Tutar (€)", min_value=0, step=5, key="h_tutar")
            with c3:
                st.write("") # Boşluk
                st.write("")
                if st.button("➕ Ekle"):
                    if kalem and tutar > 0:
                        st.session_state.harcamalar.append({"Kalem": kalem, "Tutar": tutar})
                        st.success(f"{kalem} eklendi!")
                    else:
                        st.warning("İsim ve tutar girin.")

        st.divider()

        # 2. LİSTEYİ GÖSTERME
        if len(st.session_state.harcamalar) > 0:
            row1, row2 = st.columns([2, 1])
           
            with row1:
                st.write(" **Harcama Geçmişi**")
                st.dataframe(st.session_state.harcamalar, use_container_width=True)
           
            with row2:
                toplam_aylik = sum(item['Tutar'] for item in st.session_state.harcamalar)
                st.error(f"Toplam Harcanan: {toplam_aylik} €")
               
                # Ülkeye göre limit uyarısı değişsin
                if "Almanya" in secilen_ulke:
                    limit = 934
                    msg = "Aylık bloke hesap limitini (934€) aştın!"
                else: # İtalya
                    limit = 800
                    msg = "Ortalama İtalya öğrenci bütçesini (800€) aştın!"
               
                if toplam_aylik > limit:
                    st.write(f" {msg}")
                else:
                    st.write(f" Bütçe iyi gidiyor: {limit - toplam_aylik} € kaldı.")
               
                if st.button(" Listeyi Sıfırla"):
                    st.session_state.harcamalar = []
                    st.rerun()
        else:
            st.info("Henüz bir harcama eklemedin. Yukarıdan ekleyebilirsin.")
            # --- ALT SEKME 2: AYLIK HARCAMA TAKİBİ (DİL DESTEKLİ) ---
    with butce_tab2:
        st.subheader(txt['t3_wallet_head'])
        # Ülke ismini metnin içine yerleştiriyoruz
        st.caption(txt['t3_wallet_caption'].format(country=secilen_ulke))

        # Hafıza (Session State)
        if "harcamalar" not in st.session_state:
            st.session_state.harcamalar = []

        # 1. VERİ GİRİŞ ALANI
        with st.container():
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                kalem = st.text_input(txt['t3_item_label'], key="t3_h_ad")
            with c2:
                tutar = st.number_input(txt['t3_cost_label'], min_value=0, step=5, key="t3_h_tutar")
            with c3:
                st.write("") # Boşluk
                st.write("")
                if st.button(txt['add_btn'], key="t3_gider_ekle_btn"):
                    if kalem and tutar > 0:
                        st.session_state.harcamalar.append({"Kalem": kalem, "Tutar": tutar})
                        st.success(txt['item_added'].format(item=kalem))
                    else:
                        st.warning(txt['enter_valid'])

        st.divider()

        # 2. LİSTEYİ GÖSTERME
        if len(st.session_state.harcamalar) > 0:
            row1, row2 = st.columns([2, 1])
           
            with row1:
                st.write(txt['history_head'])
                st.dataframe(st.session_state.harcamalar, use_container_width=True)
           
            with row2:
                toplam_aylik = sum(item['Tutar'] for item in st.session_state.harcamalar)
                st.error(txt['total_spent'].format(total=toplam_aylik))
               
                # Ülkeye göre limit uyarısı değişsin (Hem TR hem EN isimleri kontrol ediyoruz)
                if "Almanya" in secilen_ulke or "Germany" in secilen_ulke:
                    limit = 934
                    msg = txt['limit_msg_de']
                elif "İtalya" in secilen_ulke or "Italy" in secilen_ulke:
                    limit = 800
                    msg = txt['limit_msg_it']
                else:
                    limit = 500
                    msg = txt['limit_msg_gen']
               
                if toplam_aylik > limit:
                    st.write(f"⚠️ {msg}")
                else:
                    st.write(txt['budget_ok'].format(remaining=limit - toplam_aylik))
               
                if st.button(txt['reset_btn']):
                    st.session_state.harcamalar = []
                    st.rerun()
        else:
            st.info(txt['no_expenses'])

# --- TAB 4: SEYAHAT VE YAŞAM (ÇİFT DİLLİ) ---
with tab4:
    st.subheader(f"{secilen_ulke} {txt['t4_header']}")
   
    # İKİ GÜÇLÜ ÖZELLİK YAN YANA (DİL DESTEKLİ)
    yasam_tab1, yasam_tab2 = st.tabs(txt['t4_tabs'])

    # --- 1. AKILLI EV BULUCU ---
    with yasam_tab1:
        st.info(txt['t4_smart_info'])
        st.caption(txt['t4_smart_cap'])

        c_life1, c_life2 = st.columns([1, 1.2], gap="large")

        with c_life1:
            # Şehir seçimi
            sehir = st.selectbox(txt['t4_city_label'], aktif_veri["cities"], key="sehir_konut")
           
            # Bütçe ve Tarz
            butce_limit = st.slider(txt['t4_budget_label'], 300, 2000, 700)
            yasam_tarzi = st.multiselect(txt['t4_vibe_label'], txt['t4_vibes_list'])
           
            analiz_btn = st.button(txt['t4_btn_analyze'], type="primary")

        with c_life2:
            if analiz_btn:
                if len(yasam_tarzi) < 2:
                    st.warning(txt['t4_warn'])
                else:
                    with st.spinner(f"{sehir} {txt['t4_spin']}"):
                        try:
                            # 1. AI SEMT ANALİZİ
                            res = client.chat.completions.create(
                                model="gpt-4o",
                                messages=[{
                                    "role": "system",
                                    "content": txt['t4_p_sys_home'].format(country=secilen_ulke, instr=txt['ai_instr'])
                                },
                                {
                                    "role": "user",
                                    "content": txt['t4_p_usr_home'].format(city=sehir, budget=butce_limit, vibe=', '.join(yasam_tarzi))
                                }]
                            )
                           
                            # Sonucu Göster
                            st.success(txt['t4_success'].format(city=sehir))
                            st.markdown(f"""
                            <div style="background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #1E3A8A; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                                {res.choices[0].message.content}
                            </div>
                            """, unsafe_allow_html=True)
                           
                            # 2. AKILLI LİNKLER
                            st.markdown("---")
                            st.write(txt['t4_links_head'])
                           
                            c_lnk1, c_lnk2 = st.columns(2)
                           
                            # Ülkeye Göre Link Oluşturma (Mantık aynı kalıyor)
                            if "Almanya" in secilen_ulke:
                                link1 = f"https://www.wg-gesucht.de/wg-zimmer-in-{sehir.replace('ü','ue').replace('ö','oe')}.0.1.1.0.html?offer_filter=1&noDeact=1&rMax={butce_limit}"
                                site1 = "WG-Gesucht"
                                link2 = f"https://www.immobilienscout24.de/Suche/de/{sehir.lower()}/wohnung-mieten?price=-{butce_limit}"
                                site2 = "ImmoScout24"
                            elif "İtalya" in secilen_ulke:
                                link1 = f"https://www.idealista.it/affitto-case/{sehir.lower()}/?prezzo-massimo={butce_limit}"
                                site1 = "Idealista"
                                link2 = f"https://www.uniplaces.com/accommodation/{sehir.lower()}?budget-max={butce_limit}"
                                site2 = "Uniplaces"
                            else:
                                link1 = f"https://www.google.com/search?q=student accommodation {sehir} under {butce_limit} euro"
                                site1 = "Google"
                                link2 = f"https://www.airbnb.com/s/{sehir}/homes?price_max={butce_limit}"
                                site2 = "Airbnb"

                            with c_lnk1: st.link_button(txt['t4_search_on'].format(site=site1), link1, use_container_width=True)
                            with c_lnk2: st.link_button(txt['t4_search_on'].format(site=site2), link2, use_container_width=True)
                           
                        except: st.error(txt['err_conn'])
            else:
                st.info(txt['t4_wait_msg'])

    

    # --- 2. GEZİ VE KEŞİF (DİL DESTEKLİ) ---
    with yasam_tab2:
        st.info(txt['t4_trip_info']) # "Turist gibi değil..."

        c_gezi1, c_gezi2 = st.columns([1, 1], gap="large")
       
        with c_gezi1:
            # (Konaklama sekmesinde bir yerde olmalı)
            konaklama_sehir = st.selectbox(txt['t4_city_label'], aktif_veri["cities"], key="t4_konak_sehir")
            gezi_modu = st.radio(txt['t4_trip_mode'], txt['t4_modes'], key="t4_gezi_modu")
            rota_btn = st.button(txt['t4_btn_route'], key="t4_rota_btn")
           
        with c_gezi2:
            if rota_btn:
                with st.spinner(txt['t4_spin_route']):
                    try:
                        # AI Prompt'unu sözlükten çekip dolduruyoruz
                        final_prompt = txt['t4_prompt_trip'].format(country=secilen_ulke, city=gezi_sehir, mode=gezi_modu)
                       
                        res = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "user", "content": final_prompt}]
                        )
                        st.success(txt['t4_success_route'].format(mode=gezi_modu))
                        st.write(res.choices[0].message.content)
                       
                        # Harita Linki (Modun içindeki emojiyi veya kelimeyi kullanır)
                        # split(' ')[1] ile emojiden sonraki ilk kelimeyi alıyoruz
                        keyword = gezi_modu.split(' ')[1] if len(gezi_modu.split(' ')) > 1 else gezi_modu
                        maps_url = f"https://www.google.com/maps/search/{gezi_sehir}+{keyword}"
                       
                        st.link_button(txt['t4_map_btn'], maps_url)
                       
                    except: st.error("Hata / Error")
            else:
                st.info(txt['t4_trip_wait'])
# --- TAB 5: ÖĞRENCİ TOPLULUĞU (DÜZELTİLMİŞ & ÇİFT DİLLİ) ---
with tab5:
   
    # Sekme isimlerini sözlükten çekiyoruz
    sosyal_tab1, sosyal_tab2, sosyal_tab3 = st.tabs(txt['t5_tabs'])

    # --- 1. YOL ARKADAŞI (PROFESYONEL & FİLTRELİ) ---
    with sosyal_tab1:
        BUDDY_FILE = f"buddies_{secilen_ulke}.json"
       
        # Veri Yükleme
        if not os.path.exists(BUDDY_FILE):
            with open(BUDDY_FILE, "w", encoding="utf-8") as f: json.dump([], f)
       
        with open(BUDDY_FILE, "r", encoding="utf-8") as f:
            try: buddies = json.load(f)
            except: buddies = []

        # --- ÜST KISIM: FİLTRELEME (DİL DESTEKLİ) ---
        c_filter1, c_filter2 = st.columns([3, 1])
        with c_filter1:
            st.write(txt['buddy_find_header']) # "Kriterlerine Uygun Arkadaşı Bul"
        with c_filter2:
            # Şehre Göre Filtreleme ("Tümü" seçeneği de dilden geliyor)
            filtre_sehir = st.selectbox(txt['filter_city_label'], [txt['filter_all']] + aktif_veri["cities"])

        st.divider()

        c1, c2 = st.columns([1, 1.5], gap="large")

        # --- SOL: PROFİL OLUŞTURMA KARTI (DİL DESTEKLİ) ---
        with c1:
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #ddd; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="color:#1E3A8A; margin:0;">{txt['bud_create_title']}</h4>
                <p style="font-size:12px; color:grey;">{txt['bud_create_desc']}</p>
            </div>
            """, unsafe_allow_html=True)
           
            with st.form("buddy_pro_form", clear_on_submit=True):
                ad = st.text_input(txt['bud_inp_name'])
                bolum = st.text_input(txt['bud_inp_dept'])
                hedef = st.selectbox(txt['bud_inp_city'], aktif_veri["cities"])
                tarih = st.date_input(txt['bud_inp_date'], value=date(2025, 9, 1))
               
                # Çoklu Seçim (Seçenekler de dilden geliyor)
                ilgi_alanlari = st.multiselect(txt['bud_inp_interests'], txt['bud_interest_opts'])
               
                iletisim = st.text_input(txt['bud_inp_contact'])
               
                submitted = st.form_submit_button(txt['bud_btn_publish'])
               
                if submitted and ad:
                    yeni_profil = {
                        "Ad": ad, "Bölüm": bolum, "Şehir": hedef,
                        "Tarih": str(tarih), "İlgi": ilgi_alanlari,
                        "İletişim": iletisim, "Avatar": random.choice(["👨‍🎓", "👩‍🎓", "🧑‍💻", "👩‍🚀", "🦸‍♂️"]) # Rastgele avatar
                    }
                    buddies.append(yeni_profil)
                    with open(BUDDY_FILE, "w", encoding="utf-8") as f: json.dump(buddies, f, ensure_ascii=False, indent=4)
                    st.success(txt['bud_success'])
                    st.rerun()
        # --- SAĞ: KİŞİ KARTLARI (ÇİFT DİLLİ) ---
        with c2:
            # Başlık: "{secilen_ulke} Yolcuları" veya "{country} Travelers"
            st.write(txt['bud_list_header'].format(country=secilen_ulke))
           
            # Filtreleme Mantığı (txt['filter_all'] ile dil uyumlu kontrol)
            gosterilecekler = [b for b in buddies if filtre_sehir == txt['filter_all'] or b["Şehir"] == filtre_sehir]
           
            if not gosterilecekler:
                # Boş durum mesajı
                st.info(txt['bud_empty_msg'].format(city=filtre_sehir))
           
            # Kartları Listeleme (Tersten - En yeni en üstte)
            for kisi in reversed(gosterilecekler):
                # İlgi alanlarını güzel göstermek için yan yana diziyoruz
                etiketler = " ".join([f"<span style='background-color:#E8F0FE; color:#1E3A8A; padding:2px 8px; border-radius:10px; font-size:12px;'>{tag}</span>" for tag in kisi.get("İlgi", [])])
               
                with st.container():
                    c_av, c_detay, c_aksiyon = st.columns([0.15, 0.65, 0.2])
                   
                    with c_av:
                        # Büyük Avatar
                        st.markdown(f"<div style='font-size:40px; text-align:center;'>{kisi.get('Avatar', '👤')}</div>", unsafe_allow_html=True)
                   
                    with c_detay:
                        st.markdown(f"**{kisi['Ad']}** <span style='color:grey; font-size:12px;'>({kisi['Bölüm']})</span>", unsafe_allow_html=True)
                        st.caption(f"📍 {kisi['Şehir']} | 📅 Gidiş: {kisi['Tarih']}")
                        st.markdown(etiketler, unsafe_allow_html=True)
                       
                    with c_aksiyon:
                        st.write("") # Hizalama boşluğu
                        # Buton ismi: "Bağlan" veya "Connect"
                        if st.button(txt['bud_connect_btn'], key=f"connect_{kisi['Ad']}"):
                            # Bildirim: "İletişim: ..."
                            st.toast(txt['bud_toast_msg'].format(contact=kisi['İletişim']), icon="📩")
                           
                    st.divider()

   # --- 2. İKİNCİ EL (DİL DESTEKLİ) ---
    with sosyal_tab2:
        MARKET_FILE = f"market_{secilen_ulke}.json"
        UPLOAD_DIR = "uploads"
       
        if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)
        if not os.path.exists(MARKET_FILE):
            with open(MARKET_FILE, "w", encoding="utf-8") as f: json.dump([], f)
       
        with open(MARKET_FILE, "r", encoding="utf-8") as f:
            try: items = json.load(f)
            except: items = []

        st.warning(txt['market_security_warn']) # Güvenlik uyarısı

        col_m1, col_m2 = st.columns([1.3, 1], gap="large")
       
        # --- SOL: VİTRİN ---
        with col_m1:
            st.write(txt['market_showcase_title']) # "Vitrin"
           
            if items:
                for i, item in enumerate(reversed(items)):
                    with st.container():
                        # Görsel
                        if item.get("Gorsel") and os.path.exists(item["Gorsel"]):
                            st.image(item["Gorsel"], use_container_width=True)

                        # İlan Kartı
                        st.markdown(f"""
                        <div style="border:1px solid #ddd; padding:15px; border-radius:12px; background-color:white; margin-bottom:10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <h4 style="margin:0; color:#333;">{item['Urun']}</h4>
                                <span style="color:#1E3A8A; font-weight:bold; font-size:18px;">{item['Fiyat']} €</span>
                            </div>
                            <p style="color:grey; font-size:12px; margin:5px 0;">📍 {item['Sehir']} • 👤 {item['Satici']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                       
                        c_buy, c_del = st.columns([2, 1])
                       
                        # İLETİŞİM KISMI
                        with c_buy:
                            with st.expander(txt['market_contact_btn']): # "Satıcıyla Görüş"
                                contact_info = item.get('Iletisim', '-')
                                st.write(txt['market_contact_info'].format(info=contact_info))
                               
                                if contact_info.isdigit() and len(contact_info) > 9:
                                    wa_link = f"https://wa.me/{contact_info}"
                                    st.link_button(txt['market_whatsapp_btn'], wa_link)
                                else:
                                    st.caption(txt['market_save_num'])

                        # SİLME / BİLDİRME KISMI (AYNI KALDI)
                        with c_del:
                            aktif_kullanici = st.session_state.get("kullanici_adi", "Misafir")
                            ilan_sahibi = item.get("Satici", "")
                           
                            if aktif_kullanici == ilan_sahibi or aktif_kullanici == "Admin":
                                if st.button(txt['delete_btn'], key=f"del_market_{i}"): # "Sil"
                                    if item.get("Gorsel") and os.path.exists(item["Gorsel"]):
                                        try: os.remove(item["Gorsel"])
                                        except: pass
                                    items.pop(len(items)-1-i)
                                    with open(MARKET_FILE, "w", encoding="utf-8") as f: json.dump(items, f)
                                    st.rerun()
                            else:
                                if st.button(txt['report_btn'], key=f"rep_{i}"): # "Bildir"
                                    st.toast("Reported!", icon="🛡️")
                       
                        st.divider()
            else:
                st.info(txt['market_no_items']) # "Henüz ilan yok"
           
        
            
           
        # --- SAĞ: İLAN VERME FORMU (ÇİFT DİLLİ) ---
        with col_m2:
            st.write(txt['mkt_sell_title'])
           
            with st.form("t5_sell_item_form", clear_on_submit=True):
                urun = st.text_input(txt['mkt_inp_title'])
                fiyat = st.number_input(txt['mkt_inp_price'], min_value=0)
                sehir = st.selectbox(txt['mkt_inp_loc'], aktif_veri["cities"])
                iletisim = st.text_input(txt['mkt_inp_contact'], placeholder=txt['mkt_ph_contact'])
                foto = st.file_uploader(txt['mkt_inp_photo'], type=["jpg", "png", "jpeg"])
               
                if st.form_submit_button(txt['mkt_btn_publish']):
                    if not iletisim:
                        st.error(txt['mkt_err_contact'])
                    else:
                        gorsel_yolu = None
                        if foto:
                            # Benzersiz dosya ismi
                            dosya_adi = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{foto.name}"
                            gorsel_yolu = os.path.join(UPLOAD_DIR, dosya_adi)
                            with open(gorsel_yolu, "wb") as f: f.write(foto.getbuffer())
                       
                        items.append({
                            "Urun": urun, "Fiyat": fiyat, "Sehir": sehir,
                            "Satici": st.session_state.get("kullanici_adi", "Anonim"),
                            "Iletisim": iletisim,
                            "Gorsel": gorsel_yolu
                        })
                        with open(MARKET_FILE, "w", encoding="utf-8") as f: json.dump(items, f, ensure_ascii=False, indent=4)
                        st.success(txt['mkt_success_msg'])
                        st.rerun()
    # --- 3. SOSYAL AKIŞ (INSTAGRAM TARZI & DİL DESTEKLİ) ---
    with sosyal_tab3:
        SOCIAL_FILE = f"social_{secilen_ulke}.json"
        UPLOAD_DIR = "uploads"
       
        # Klasör ve Dosya Kontrolü
        if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)
        if not os.path.exists(SOCIAL_FILE):
            with open(SOCIAL_FILE, "w", encoding="utf-8") as f: json.dump([], f)

        # Veri Yükleme/Kaydetme
        def load_posts():
            try:
                with open(SOCIAL_FILE, "r", encoding="utf-8") as f: return json.load(f)
            except: return []

        def save_posts(posts):
            with open(SOCIAL_FILE, "w", encoding="utf-8") as f:
                json.dump(posts, f, ensure_ascii=False, indent=4)

        # --- YENİ GÖNDERİ OLUŞTURMA ---
        with st.expander(txt['sf_new_post_title'], expanded=False): # "Yeni Gönderi Paylaş"
            with st.form("new_post_form", clear_on_submit=True):
                caption = st.text_area(txt['sf_caption_ph'], placeholder="Berlin...") # "Ne düşünüyorsun?"
                photo = st.file_uploader(txt['sf_photo_label'], type=["jpg", "png", "jpeg"]) # "Fotoğraf Ekle"
               
                if st.form_submit_button(txt['sf_btn_share']): # "Paylaş"
                    img_path = None
                    if photo:
                        img_path = os.path.join(UPLOAD_DIR, f"post_{datetime.now().timestamp()}_{photo.name}")
                        with open(img_path, "wb") as f: f.write(photo.getbuffer())
                   
                    user = st.session_state.get("kullanici_adi", "Anonim")
                   
                    posts = load_posts()
                    posts.append({
                        "id": str(datetime.now().timestamp()),
                        "user": user,
                        "caption": caption,
                        "image": img_path,
                        "likes": 0,
                        "comments": [],
                        "date": datetime.now().strftime("%d.%m %H:%M")
                    })
                    save_posts(posts)
                    st.success(txt['sf_success']) # "Paylaşıldı!"
                    st.rerun()

        st.markdown("---")

       

        # --- AKIŞ (FEED) (DİL DESTEKLİ) ---
    posts = load_posts()

    if not posts:
            st.info(txt['sf_empty_msg']) # "Henüz gönderi yok..."
    else:
            # En yeniler en üstte
            for i, post in enumerate(reversed(posts)):
                # KART TASARIMI
                with st.container():
                    # Başlık (Kullanıcı Adı)
                    c_av, c_user = st.columns([0.1, 0.9])
                    with c_av: st.write("👤")
                    with c_user: st.markdown(f"**{post['user']}** <span style='color:grey; font-size:12px;'>• {post['date']}</span>", unsafe_allow_html=True)
                
            # Fotoğraf (Varsa)
            if post.get("image") and os.path.exists(post["image"]):
                st.image(post["image"], use_container_width=True)
           
            # Açıklama
            if post["caption"]:
                st.write(post["caption"])
           
            # --- ETKİLEŞİM BUTONLARI (BEĞENİ & YORUM) ---
            c_like, c_com_count = st.columns([0.2, 0.8])
           
            # Beğeni Butonu
            btn_label = f"❤️ {post['likes']}"
            if c_like.button(btn_label, key=f"like_{post['id']}"):
                # Beğeni sayısını artır ve kaydet
                real_index = len(posts) - 1 - i
                posts[real_index]["likes"] += 1
                save_posts(posts)
                st.rerun()

            # Yorumları Göster
            comment_count = len(post["comments"])
            # Caption: "{count} Yorum" veya "{count} Comments"
            c_com_count.caption(txt['sf_comments_count'].format(count=comment_count))
           
            # Yorumlar Alanı (Expander içinde)
            with st.expander(txt['sf_expand_comments']): # "Yorumları Gör / Yaz"
                # Eski yorumlar
                for com in post["comments"]:
                    st.markdown(f"**{com['user']}:** {com['text']}")
               
                # Yeni Yorum Formu
                with st.form(key=f"com_form_{post['id']}", clear_on_submit=True):
                    # Input: "Yorum ekle..." ve placeholder
                    new_comment = st.text_input(txt['sf_comment_ph'], placeholder=txt['sf_comment_holder'])
                    if st.form_submit_button(txt['sf_btn_send']): # "Gönder"
                        real_index = len(posts) - 1 - i
                        current_user = st.session_state.get("kullanici_adi", "Anonim")
                        posts[real_index]["comments"].append({"user": current_user, "text": new_comment})
                        save_posts(posts)
                        st.rerun()
           
            st.divider() # Gönderiler arası çizgi
# --- TAB 6: S.O.S ACİL DURUM (FİNAL DÜZELTİLMİŞ) ---
with tab6:
    st.error(f"🚨 **{secilen_ulke} {txt['sos_header']}**")
    st.caption(txt['sos_caption'])

    # --- ÜLKEYE ÖZEL ACİL DURUM VERİLERİ ---
    # Not: Anahtarların (Key), yukarıdaki 'country_data' ile uyumlu olması için emojileri kaldırdık.
    # Ancak senin 'secilen_ulke' değişkenin emojili geliyorsa (Örn: "🇩🇪 Germany"),
    # aşağıda .get() kullanırken buna dikkat edeceğiz.
    
    acil_bilgiler = {
        " Germany": {
            "polis": "110", "ambulans": "112", "konsolosluk": "+49 30 896 80 211",
            "cumleler": [
                (txt['sos_card_doctor_head'], "Ich brauche einen Arzt!"),
                (txt['sos_card_lost_head'], "Mein Pass wurde gestohlen!"),
                (txt['sos_card_police_head'], "Hilfe! Bitte helfen Sie mir!"),
                ("Speaking", "Ich spreche kein Deutsch.")
            ]
        },
        " Italy": {
            "polis": "112 (Carabinieri)", "ambulans": "118", "konsolosluk": "+39 06 445 941",
            "cumleler": [
                (txt['sos_card_doctor_head'], "Ho bisogno di un dottore!"),
                (txt['sos_card_lost_head'], "Il mio passaporto è stato rubato!"),
                (txt['sos_card_police_head'], "Aiuto! Mi aiuti per favore!"),
                ("Speaking", "Non parlo italiano.")
            ]
        },
        " Spain": {
            "polis": "091", "ambulans": "061", "konsolosluk": "+34 913 103 904",
            "cumleler": [
                (txt['sos_card_doctor_head'], "Necesito un médico!"),
                (txt['sos_card_lost_head'], "Me han robado el pasaporte!"),
                (txt['sos_card_police_head'], "¡Ayuda! ¡Por favor ayúdeme!"),
                ("Speaking", "No hablo español.")
            ]
        },
        " France": {
            "polis": "17", "ambulans": "15", "konsolosluk": "+33 1 53 92 71 11",
            "cumleler": [
                (txt['sos_card_doctor_head'], "J'ai besoin d'un médecin!"),
                (txt['sos_card_lost_head'], "Mon passeport a été volé!"),
                (txt['sos_card_police_head'], "Aidez-moi, s'il vous plaît!"),
                ("Speaking", "Je ne parle pas français.")
            ]
        },
        " Poland": {
            "polis": "997", "ambulans": "999", "konsolosluk": "+48 22 854 61 10",
            "cumleler": [
                (txt['sos_card_doctor_head'], "Potrzebuję lekarza!"),
                (txt['sos_card_lost_head'], "Skradziono mi paszport!"),
                (txt['sos_card_police_head'], "Pomocy! Proszę mi pomóc!"),
                ("Speaking", "Nie mówię po polsku.")
            ]
        }
    }
    
    # Seçilen ülkenin isminden emojiyi ve boşluğu temizleyip saf ismini alıyoruz (Örn: "🇩🇪 Germany" -> "Germany")
    saf_ulke_ismi = secilen_ulke.split(" ")[-1] 
    
    # Veriyi Çekme (Hata olursa Germany varsayılan)
    acil = acil_bilgiler.get(saf_ulke_ismi, acil_bilgiler.get(" Germany"))
    
    # Eğer veri gelmezse hata vermemesi için koruma
    if not acil:
         # Fallback (Yedek) olarak Almanya verisini yükle
         acil = acil_bilgiler[" Germany"]

    c_sos1, c_sos2 = st.columns([1, 1], gap="large")

    # --- SOL: AI DANIŞMAN ---
    with c_sos1:
        st.write(txt['sos_advisor_head'])
        
        # Radyo butonuna benzersiz key ekledik
        durum = st.radio(txt['sos_radio_label'], txt['sos_radio_opts'], key="sos_durum_radio") 
        
        # Butona benzersiz key ekledik
        if st.button(txt['sos_help_btn'], key="sos_help_button"):
            with st.spinner(txt['sos_spinner']):
                try:
                    # System prompt dilden çekildi
                    sys_prompt = txt['sos_sys_prompt'].format(country=secilen_ulke, situation=durum)

                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{
                            "role": "system", 
                            "content": sys_prompt
                        }]
                    )
                    st.warning(txt['sos_warning_title'])
                    st.write(res.choices[0].message.content)
                except: st.error(txt['sos_internet_err'])

    # --- SAĞ: NUMARALAR VE KARTLAR ---
    with c_sos2:
        st.info(f"📞 **{secilen_ulke} {txt['sos_numbers_title']}**")
        
        st.markdown(f"""
        -  **{txt['sos_police']}:** {acil['polis']}
        -  **{txt['sos_ambulance']}:** {acil['ambulans']}
        -  **{txt['sos_consulate']}:** {acil['konsolosluk']}
        -  **{txt['sos_eu_emergency']}:** 112
        """)

        st.divider()
        st.write(txt['sos_cards_head'])
        st.caption(txt['sos_cards_caption'])
        
        # Kartları Döngüyle Oluştur
        if 'cumleler' in acil:
            for baslik, metin in acil['cumleler']:
                with st.expander(baslik):
                    st.code(metin, language="text")
                    st.caption(txt['sos_card_general_ask'])
                   
st.divider()
st.caption(txt['footer_legal'])

        