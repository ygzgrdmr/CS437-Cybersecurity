import requests
from flask import make_response, render_template, request, redirect, url_for, flash, current_app,abort, send_from_directory
from flask_login import current_user,login_user, login_required, logout_user
from flask_login import LoginManager
from flask_login import UserMixin
from lxml import etree
from math import ceil
import os
import logging
import feedparser
import json
from flask import Flask, render_template, request, redirect, url_for
from func import check_user_credentials, fetch_rss_feeds, calculate_page_range
from models import User
from werkzeug.utils import secure_filename
from xml.etree import ElementTree as ET
from database import db, Article
import html
from werkzeug.security import generate_password_hash, check_password_hash
from flask_caching import Cache
from models import User, db

# Loglama yapılandırması için tam yol
log_file_path = '/Users/yagizgurdamar/Desktop/cs437/Assignment/application.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



UPLOAD_FOLDER = "/Users/yagizgurdamar/Desktop/cs437/Assignment"
users_json_path = "/Users/yagizgurdamar/Desktop/cs437/Assignment/users.json"




#rss linkleri
""" 
rss_feeds  = [

"https://www.ntv.com.tr/gundem.rss",
"https://www.ntv.com.tr/dunya-kupasi-2018.rss",
"https://www.ntv.com.tr/turkiye.rss",
"https://www.ntv.com.tr/dunya.rss",
"https://www.ntv.com.tr/ekonomi.rss",
"https://www.ntv.com.tr/spor.rss",
"https://www.ntv.com.tr/teknoloji.rss",
"https://www.ntv.com.tr/yasam.rss",
"https://www.ntv.com.tr/saglik.rss",
"https://www.ntv.com.tr/egitim.rss",
"https://www.aa.com.tr/tr/rss/default?cat=guncel",
"http://www.anayurtgazetesi.com/sondakika.xml",
"http://www.cumhuriyet.com.tr/rss/son_dakika.xml",
"http://www.cumhuriyet.com.tr/rss/6.xml",
"http://www.cumhuriyet.com.tr/rss/17.xml",
"http://www.cumhuriyet.com.tr/rss/73.xml",
"http://www.cumhuriyet.com.tr/rss/24.xml",
"http://www.cumhuriyet.com.tr/rss/32.xml",
"http://www.cumhuriyet.com.tr/rss/33.xml",
"http://www.cumhuriyet.com.tr/rss/34.xml",
"http://www.cumhuriyet.com.tr/rss/35.xml",
"http://www.cumhuriyet.com.tr/rss/36.xml",
"http://www.cumhuriyet.com.tr/rss/46.xml",
"http://www.cumhuriyet.com.tr/rss/70.xml",
"http://www.cumhuriyet.com.tr/rss/19.xml",
"http://www.cumhuriyet.com.tr/rss/7.xml",
"http://www.cumhuriyet.com.tr/rss/14.xml",
"http://www.cumhuriyet.com.tr/rss/15.xml",
"http://www.cumhuriyet.com.tr/rss/16.xml",
"http://www.cumhuriyet.com.tr/rss/20.xml",
"http://www.cumhuriyet.com.tr/rss/72.xml",
"http://www.cumhuriyet.com.tr/rss/12.xml",
"http://www.cumhuriyet.com.tr/rss/3.xml",
"http://www.cumhuriyet.com.tr/rss/9.xml",
"http://www.cumhuriyet.com.tr/rss/11.xml",
"http://www.cumhuriyet.com.tr/rss/10.xml",
"https://www.dunya.com/rss?dunya",
"http://www.haberturk.com/rss",
"http://www.hurriyet.com.tr/rss/anasayfa",
"http://www.hurriyet.com.tr/rss/gundem",
"http://www.hurriyet.com.tr/rss/ekonomi",
"http://www.hurriyet.com.tr/rss/magazin",
"http://www.hurriyet.com.tr/rss/spor",
"http://www.hurriyet.com.tr/rss/dunya",
"http://www.hurriyet.com.tr/rss/teknoloji",
"http://www.hurriyet.com.tr/rss/saglik",
"http://www.hurriyet.com.tr/rss/astroloji",
"http://www.milatgazetesi.com/rss.php",
"http://www.milliyet.com.tr/rss/rssNew/gundemRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/kitapRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/egitimRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/dunyaRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/ekonomiRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/siyasetRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/teknolojiRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/milliyettatilRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/teknolojiRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/saglikRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/SonDakikaRss.xml",
" https://www.sabah.com.tr/rss/ekonomi.xml",
"https://www.sabah.com.tr/rss/spor.xml",
"https://www.sabah.com.tr/rss/gundem.xml",
"https://www.sabah.com.tr/rss/yasam.xml",
"https://www.sabah.com.tr/rss/dunya.xml",
"https://www.sabah.com.tr/rss/teknoloji.xml",
"https://www.sabah.com.tr/rss/anasayfa.xml",
"https://www.sabah.com.tr/rss/saglik.xml",
"https://www.sabah.com.tr/rss/gununicinden.xml",
"https://www.sabah.com.tr/rss/sondakika.xml",
"https://www.sabah.com.tr/rss/kultur-sanat.xml",
"http://www.star.com.tr/rss/rss.asp",
"http://www.star.com.tr/rss/rss.asp?cid=500",
"http://www.star.com.tr/rss/rss.asp?cid=13",
"http://www.star.com.tr/rss/rss.asp?cid=15",
"http://www.star.com.tr/rss/rss.asp?cid=16",
"http://www.star.com.tr/rss/rss.asp?cid=17",
"http://www.star.com.tr/rss/rss.asp?cid=19",
"http://www.star.com.tr/rss/rss.asp?cid=125",
"http://www.star.com.tr/rss/rss.asp?cid=223",
"http://www.star.com.tr/rss/rss.asp?cid=130",
"http://www.star.com.tr/rss/rss.asp?cid=170",
"https://www.takvim.com.tr/rss/anasayfa.xml",
"https://www.takvim.com.tr/rss/son24saat.xml",
"https://www.takvim.com.tr/rss/guncel.xml",
"https://www.takvim.com.tr/rss/ekonomi.xml",
"https://www.takvim.com.tr/rss/spor.xml",
"https://www.takvim.com.tr/rss/yasam.xml",
"http://www.turkiyegazetesi.com.tr/rss/rss.xml",
"http://mix.chimpfeedr.com/68482-Vatan-Gazetesi",
"https://www.yeniakit.com.tr/rss/haber",
"https://www.yeniakit.com.tr/rss/haber/ekonomi",
"https://www.yeniakit.com.tr/rss/haber/gunun-mansetleri",
"https://www.yeniakit.com.tr/rss/haber/bugunku-akit",
"https://www.yeniakit.com.tr/rss/haber/ozel-haber",
"https://www.yeniakit.com.tr/rss/haber/gundem",
"https://www.yeniakit.com.tr/rss/haber/siyaset",
"https://www.yeniakit.com.tr/rss/haber/dunya",
"https://www.yeniakit.com.tr/rss/haber/teknoloji",
"https://www.yeniakit.com.tr/rss/haber/aktuel",
"https://www.yeniakit.com.tr/rss/haber/kultur-sanat",
"https://www.yeniakit.com.tr/rss/haber/saglik",
"https://www.yeniakit.com.tr/rss/haber/medya",
"https://www.yeniakit.com.tr/rss/haber/yasam",

"https://www.yeniakit.com.tr/rss/haber/yerel",
"https://www.yeniakit.com.tr/rss/haber/egitim",
"https://www.yeniakit.com.tr/rss/video/bilim-teknoloji",
"https://www.yeniakit.com.tr/rss/video/15temmuz",
"https://www.yeniakit.com.tr/rss/video/cocuk-egitim",
"https://www.yeniakit.com.tr/rss/video/dunya",
"https://www.yeniakit.com.tr/rss/video/ekonomi",
"https://www.yeniakit.com.tr/rss/video/emlak-rehberi",
"https://www.yeniakit.com.tr/rss/video/gezi",
"https://www.yeniakit.com.tr/rss/video/guncel",
"https://www.yeniakit.com.tr/rss/video/gundem",
"https://www.yeniakit.com.tr/rss/video/hayat-aktuel",
"https://www.yeniakit.com.tr/rss/video/islam",
"https://www.yeniakit.com.tr/rss/video/kultur-sanat",
"https://www.yeniakit.com.tr/rss/video/medya",
"https://www.yeniakit.com.tr/rss/video/ramazan",
"https://www.yeniakit.com.tr/rss/video/siyaset",
"https://www.yeniakit.com.tr/rss/video/spor",
"https://www.yeniakit.com.tr/rss/video/trafik-kazalari",
"https://www.yeniakit.com.tr/rss/video/turkiye",
"https://www.yeniakit.com.tr/rss/video/yasam",
"https://www.yeniakit.com.tr/rss/video/yerel",
"https://www.yeniasir.com.tr/rss/anasayfa.xml",
"http://www.yenimesaj.com.tr/rss.php",
"https://www.yenisafak.com/Rss",
"www.yenisafak.com/rss?xml=manset",
"www.yenisafak.com/rss?xml=gundem",
"www.yenisafak.com/rss?xml=spor",
"www.yenisafak.com/rss?xml=ekonomi",
"www.yenisafak.com/rss?xml=teknoloji",
"www.yenisafak.com/rss?xml=hayat",
"www.yenisafak.com/rss?xml=dunya",
"www.yenisafak.com/rss?xml=yazarlar",
"http://www.yurtgazetesi.com.tr/rss.php",
"https://www.ahaber.com.tr/rss/anasayfa.xml",
"https://www.ahaber.com.tr/rss/gundem.xml",
"https://www.ahaber.com.tr/rss/ekonomi.xml",
"https://www.ahaber.com.tr/rss/spor.xml",
"https://www.ahaber.com.tr/rss/yasam.xml",
"https://www.ahaber.com.tr/rss/dunya.xml",
"https://www.ahaber.com.tr/rss/son24saat.xml",
"https://www.ahaber.com.tr/rss/teknoloji.xml",
"https://www.ahaber.com.tr/rss/haberler.xml",
"https://www.ahaber.com.tr/rss/tarih.xml",
"https://www.ahaber.com.tr/rss/analiz.xml",
"https://www.ahaber.com.tr/rss/saglik.xml",
"https://www.cnnturk.com/feed/rss/all/news",
"https://www.cnnturk.com/feed/rss/turkiye/news",
"https://www.cnnturk.com/feed/rss/dunya/news",
"https://www.cnnturk.com/feed/rss/kultur-sanat/news",
"https://www.cnnturk.com/feed/rss/bilim-teknoloji/news",
"https://www.cnnturk.com/feed/rss/ekonomi/news",
"https://www.cnnturk.com/feed/rss/spor/news",
"https://www.cnnturk.com/feed/rss/saglik/news",
"https://www.cnnturk.com/feed/rss/all/gallery",
"https://www.cnnturk.com/feed/rss/turkiye/gallery",
"https://www.cnnturk.com/feed/rss/dunya/gallery",
"https://www.cnnturk.com/feed/rss/kultur-sanat/gallery",
"https://www.cnnturk.com/feed/rss/bilim-teknoloji/gallery",
"https://www.cnnturk.com/feed/rss/yasam/gallery",
"https://www.cnnturk.com/feed/rss/ekonomi/gallery",
"https://www.cnnturk.com/feed/rss/saglik/gallery",
"http://www.haberturk.com/rss",
"http://www.trthaber.com/sondakika.rss",
"http://www.ulusal.com.tr/rss.php",
"http://www.acikgazete.com/feed/",
"https://www.ajanshaber.com/rss",
"http://www.aygazete.com/rss/gundem-haberleri",
"http://feeds.bbci.co.uk/turkce/rss.xml",
"http://rss.dw.com/rdf/rss-tur-all",
"http://www.ensonhaber.com/rss/ensonhaber.xml",

"http://sinema.mynet.com/rss/RSS-enyeniler/rss.xml",
"http://spor.mynet.com/rss",
"http://www.mynet.com/haber/rss/sondakika",
"http://www.mynet.com/haber/rss/gununozeti/",
"http://www.mynet.com/haber/rss/kategori/politika/",
"http://www.mynet.com/haber/rss/kategori/teknoloji/",
"http://www.mynet.com/haber/rss/kategori/dunya/",
"http://www.mynet.com/haber/rss/kategori/yasam/",
"http://www.mynet.com/haber/rss/kategori/magazin/",
"http://www.mynet.com/haber/rss/kategori/saglik/",
"http://yurthaber.mynet.com/rss/kategori/ana/rss.xml",
"https://tr.sputniknews.com/export/rss2/archive/index.xml",
"http://www.turkiyehaberajansi.com/rss.xml",
"http://www.internethaber.com/rss",
"http://www.finansgundem.com/rss",
"https://www.tobb.org.tr/Sayfalar/RssFeeder.php?List=Haberler",
"https://www.tobb.org.tr/Sayfalar/RssFeeder.php?List=DuyurularListesi",
"https://www.tobb.org.tr/Sayfalar/RssFeeder.php?List=MansetListesi",
"http://bigpara.hurriyet.com.tr/rss/",
"http://www.ekoseyir.com/rss/piyasalar/248.xml"
]


"""

rss_feeds  = [
"https://www.yorku.ca/yfile/rss/yfile_latest_issues.rss",
"http://vetjournal.ankara.edu.tr/tr/pub/rss/lastissue/en",
"http://vetjournal.ankara.edu.tr/tr/pub/rss/lastissue/tr",
"https://www.fakultehaber.com/rss_universite_5.xml",
"https://www.fakultehaber.com/rss_akademik_12.xml",
"https://www.ntv.com.tr/gundem.rss",
"https://www.ntv.com.tr/turkiye.rss",
"https://www.ntv.com.tr/dunya.rss",
"https://www.ntv.com.tr/ekonomi.rss",
"https://www.ntv.com.tr/spor.rss",
"https://www.ntv.com.tr/teknoloji.rss",
"https://www.ntv.com.tr/yasam.rss",
"https://www.ntv.com.tr/saglik.rss",
"https://www.ntv.com.tr/egitim.rss",
"https://www.aa.com.tr/tr/rss/default?cat=guncel",
"http://www.anayurtgazetesi.com/sondakika.xml",
"http://www.cumhuriyet.com.tr/rss/son_dakika.xml",
"http://www.cumhuriyet.com.tr/rss/6.xml",
"http://www.cumhuriyet.com.tr/rss/17.xml",
"http://www.cumhuriyet.com.tr/rss/73.xml",
"http://www.cumhuriyet.com.tr/rss/24.xml",

"http://www.cumhuriyet.com.tr/rss/3.xml",
"http://www.cumhuriyet.com.tr/rss/9.xml",
"http://www.cumhuriyet.com.tr/rss/11.xml",
"http://www.cumhuriyet.com.tr/rss/10.xml",
"https://www.dunya.com/rss?dunya",
"http://www.haberturk.com/rss",
"http://www.hurriyet.com.tr/rss/anasayfa",
"http://www.hurriyet.com.tr/rss/gundem",
"http://www.hurriyet.com.tr/rss/ekonomi",

"http://www.hurriyet.com.tr/rss/dunya",
"http://www.hurriyet.com.tr/rss/teknoloji",
"http://www.hurriyet.com.tr/rss/saglik",
"http://www.hurriyet.com.tr/rss/astroloji",
"http://www.milatgazetesi.com/rss.php",
"http://www.milliyet.com.tr/rss/rssNew/gundemRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/kitapRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/egitimRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/dunyaRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/ekonomiRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/siyasetRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/teknolojiRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/milliyettatilRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/teknolojiRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/saglikRss.xml",
"http://www.milliyet.com.tr/rss/rssNew/SonDakikaRss.xml",
" https://www.sabah.com.tr/rss/ekonomi.xml",
"https://www.sabah.com.tr/rss/spor.xml",
"https://www.sabah.com.tr/rss/gundem.xml",
"https://www.sabah.com.tr/rss/yasam.xml",
"https://www.sabah.com.tr/rss/dunya.xml",
"https://www.sabah.com.tr/rss/teknoloji.xml",
"https://www.sabah.com.tr/rss/anasayfa.xml",
"https://www.sabah.com.tr/rss/saglik.xml",
"https://www.sabah.com.tr/rss/gununicinden.xml",
"https://www.sabah.com.tr/rss/sondakika.xml",
"https://www.sabah.com.tr/rss/kultur-sanat.xml",
"http://www.star.com.tr/rss/rss.asp",
"http://www.star.com.tr/rss/rss.asp?cid=500",
"http://www.star.com.tr/rss/rss.asp?cid=13",
"http://www.star.com.tr/rss/rss.asp?cid=15",
"http://www.star.com.tr/rss/rss.asp?cid=16",
"http://www.star.com.tr/rss/rss.asp?cid=17",
"http://www.star.com.tr/rss/rss.asp?cid=19",
"http://www.star.com.tr/rss/rss.asp?cid=125",
"http://www.star.com.tr/rss/rss.asp?cid=223",
"http://www.star.com.tr/rss/rss.asp?cid=130",
"http://www.star.com.tr/rss/rss.asp?cid=170",
"https://www.takvim.com.tr/rss/anasayfa.xml",
"https://www.takvim.com.tr/rss/son24saat.xml",
"https://www.takvim.com.tr/rss/guncel.xml",
"https://www.takvim.com.tr/rss/ekonomi.xml",
"https://www.takvim.com.tr/rss/spor.xml",
"https://www.takvim.com.tr/rss/yasam.xml",
"http://www.turkiyegazetesi.com.tr/rss/rss.xml",


"https://www.cnnturk.com/feed/rss/all/news",
"https://www.cnnturk.com/feed/rss/turkiye/news",
"https://www.cnnturk.com/feed/rss/dunya/news",
"https://www.cnnturk.com/feed/rss/kultur-sanat/news",
"https://www.cnnturk.com/feed/rss/bilim-teknoloji/news",
"https://www.cnnturk.com/feed/rss/ekonomi/news",
"https://www.cnnturk.com/feed/rss/spor/news",
"https://www.cnnturk.com/feed/rss/saglik/news",
"https://www.cnnturk.com/feed/rss/all/gallery",
"https://www.cnnturk.com/feed/rss/turkiye/gallery",

"http://www.haberturk.com/rss",
"http://www.trthaber.com/sondakika.rss",
"http://www.aygazete.com/rss/gundem-haberleri",
"http://feeds.bbci.co.uk/turkce/rss.xml",
"http://rss.dw.com/rdf/rss-tur-all",



]

keywords = [
    "üniversite", "fakülte", "akademik", "öğrenci", "kampüs", "profesör",
     "İTÜ", "BOĞAZİÇİ", "ODTÜ", "KOÇ Üniversitesi", "Koç Üniversitesi","İstanbul Teknik Üniversitesi",
    "Orta Doğu Teknik Üniversitesi","BAU", "Bilgi Üniversitesi","Ankara Üniversitesi","MSÜ","Marmara Üniversitesi",
    "İstanbul Üniversitesi",
    "Sabancı Üniversitesi", "burs",  "mezuniyet", "lisans", "ön lisans",
    "yüksek lisans", "doktora", "tez", "araştırma", "bilimsel", "akademisyen",
    "üniversite hastanesi", "derslik", "laboratuvar", "konferans",
    "seminer",  "öğrenci kulübü", "dekan", "fakülte", "bölüm",
    "anabilim dalı", "bilim", "teknoloji", "mühendislik", "tıp", "hukuk", "işletme",
    "eğitim fakültesi", "mimarlık", "sanat", "sosyal bilimler", "felsefe", "tarih",
    "psikoloji", "sosyoloji", "siyaset bilimi", "uluslararası ilişkiler", "ekonomi",
    "finans", "matematik", "fizik", "kimya", "biyoloji", "diş hekimliği",
    "yabancı diller", "çeviri", "edebiyat", "şehir ve bölge planlama", "peyzaj mimarlığı",
     "veterinerlik", "denizcilik",
     "spor bilimleri",   "psikolojik danışmanlık",
    "hemşirelik", "ebelik", "beslenme ve diyetetik", "fizyoterapi", "iş sağlığı ve güvenliği",
    "çevre mühendisliği", "gıda mühendisliği", "endüstri mühendisliği", "bilgisayar mühendisliği",
    "yazılım mühendisliği", "makine mühendisliği", "elektrik-elektronik mühendisliği",
    "insan kaynakları", "pazarlama", "reklamcılık", "girişimcilik", "yenilikçilik",
    "kariyer planlama", "staj olanakları", "çift anadal", "yandal", "değişim programları",
    "Erasmus", "üniversite rehberi", "üniversite sıralamaları",
    "üniversite yorumları", "kampüs yaşamı", "öğrenci etkinlikleri", "akademik takvim",
    "sınav takvimi", "burslar", "öğrenci işleri", "öğrenci konseyi", "mezun dernekleri",
    "akademik yayınlar", "üniversite dergileri", "üniversite haberleri", "üniversite projeleri",
    "üniversite işbirlikleri", "sanayi ile işbirliği", "kariyer merkezi", "öğrenci danışmanlığı",
    "alumni", "mezunlar ağı"
]



news_id_counter = 1
news_storage = {}

def init_routes(app,cache):
    @app.route('/')
    def home():
        user_ip = request.remote_addr
        user_agent = request.user_agent.string
        logging.info(f"Ana sayfaya erişim: IP: {user_ip}, User Agent: {user_agent}")
        return render_template('home.html')

        # LoginManager
        login_manager = LoginManager()
        login_manager.init_app(app)

        # load_user callback'ini tanımla
        @login_manager.user_loader
        def load_user(user_id):
            return User.get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                logging.info(f"Successful login: {user.username}")
                return redirect(url_for('add_news'))  # Or wherever you want to redirect after a successful login
            else:
                flash('Invalid username or password')
                logging.warning(f"Failed login attempt for {username}")
                return redirect(url_for('login'))
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            name = request.form.get('name')  # Adjust these lines
            surname = request.form.get('surname')
            age = request.form.get('age')

            hashed_password = generate_password_hash(password)
            existing_user = User.query.filter_by(username=username).first()
            if existing_user is None:
                new_user = User(username=username, password=hashed_password, name=name, surname=surname, age=age)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful')
                logging.info(f"New user registered: {username}")
                return redirect(url_for('login'))
            else:
                flash('Username already taken')
                logging.warning(f"Attempt to register with an already taken username: {username}")
                return redirect(url_for('register'))
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        logout_user()
        logging.info(f"Çıkış yapıldı!")
        return redirect(url_for('home'))

    def parse_xml(file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Tüm elementleri içeren bir listeyi döndür
            news_items = []
            for elem in root.iter():
                if elem.text:  # Eğer element metin içeriyorsa, tag ve text'i listeye ekle
                    text = elem.text.strip()
                    news_items.append((elem.tag, text))
                else:  # Eğer element metin içermiyorsa, sadece tag'i ekle
                    news_items.append((elem.tag, None))

            return news_items
        except ET.ParseError as e:
            logging.error(f"XML parsing error for file {file_path}: {e}")
            return []

    @app.route('/add_news', methods=['GET', 'POST'])
    @login_required
    def add_news():
        global news_id_counter
        if request.method == 'POST':
            file = request.files.get('file')
            if file:
                logging.info(f"File received: {file.filename}")
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    logging.info(f"File saved: {file_path}")

                    try:
                        parsed_content = parse_xml(file_path)
                        news_storage[news_id_counter] = {
                            'id': news_id_counter,
                            'filename': filename,
                            'path': file_path,
                            'uploader': current_user.id,
                            'content': parsed_content
                        }
                        news_id_counter += 1
                        flash(f'Your file has been successfully uploaded. News ID: {news_id_counter - 1}', 'success')
                        logging.info(f"News added successfully: News ID: {news_id_counter - 1}")
                    except etree.XMLSyntaxError as e:
                        logging.error(f"XML parsing error: {e}, File: {filename}, User: {current_user.id}")
                        flash('XML parsing error occurred. Please check the file and try again.', 'error')
                else:
                    logging.warning(f"Invalid file type attempted to upload: {file.filename}")
                    flash('Invalid file type. Please upload an XML file.', 'error')
            else:
                logging.warning("No file received in the request.")
                flash('No file provided.', 'error')

            return redirect(url_for('add_news'))
        else:
            return render_template('add_news.html')

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xml'}

    @app.route('/news', methods=['GET'])
    @login_required
    def show_news():
        query = request.args.get('query')
        try:
            articles = fetch_rss_feeds(rss_feeds, keywords)
            uploaded_news = list(news_storage.values())

            if query:
                query = query.lower()
                articles = [article for article in articles if query in article.title.lower()]
                uploaded_news = [
                    news_item for news_item in uploaded_news
                    if query in news_item.get('content', '').lower()
                ]

            for article in articles:
                article.title = html.unescape(article.title)
                article.summary = html.unescape(article.summary)

            for news_item in uploaded_news:
                news_item['content'] = html.unescape(news_item.get('content', ''))

            return render_template('news.html', articles=articles, uploaded_news=uploaded_news)
        except Exception as e:
            logging.error(f"General error on news page: {e}")
            flash('An error occurred, please try again later.')
            return redirect(url_for('home'))

    @app.route('/remove_news/<int:article_id>', methods=['POST'])
    @login_required
    def remove_news(article_id):
        if current_user.username == 'admin':  # Replace with your admin check
            if article_id in news_storage:
                del news_storage[article_id]
                flash('News article removed successfully.', 'success')
                logging.info(f"Article removed: {article_id}")
            else:
                flash('No article found with the provided ID.', 'error')
        else:
            flash('You do not have permission to perform this action.', 'error')

        return redirect(url_for('show_news'))

    @app.route('/profile')
    @login_required
    def profile():
        user_info = User.query.get(current_user.get_id())

        if not user_info:
            flash('Kullanıcı bilgisi bulunamadı.', 'error')
            return redirect(url_for('home'))

        # Use user_info to access user details like user_info.username, user_info.age, etc.
        return render_template('profile.html', user_info=user_info)
    @app.errorhandler(500)
    def internal_error(error):
        user_ip = request.remote_addr
        logging.error(f"Sunucu hatası: {error}, IP: {user_ip}")
        return "Bir hata oluştu", 500

    @app.route('/monitoring')
    def monitoring():
        # Log dosyasının tam yolu
        log_file_path = '/Users/yagizgurdamar/Desktop/cs437/Assignment/application.log'

        try:
            with open(log_file_path, 'r') as file:
                log_data = file.readlines()
                log_data = log_data[-30:]
        except FileNotFoundError:
            log_data = ["Log file not found."]

        return render_template('monitoring.html', log_data=log_data)

