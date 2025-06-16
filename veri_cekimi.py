from google_play_scraper import app, search
import pandas as pd
import time

def get_app_data(package_name):
    try:
        details = app(package_name, lang='en', country='us')
        return {
            'App ID': package_name,
            'Title': details.get('title'),
            'Description': details.get('description'),
            'Category': details.get('genre'),
            'Rating': details.get('score'),
            'Reviews': details.get('reviews'),
            'Installs': details.get('installs'),
            'Type': 'Free' if details.get('free') else 'Paid',
            'Price': details.get('price'),
            'Content Rating': details.get('contentRating'),
        }
    except Exception as e:
        print(f"Hata: {package_name} verisi alınamadı: {e}")
        return None

def fetch_top_apps_by_search(keyword, max_count=30):
    try:
        results = search(keyword, lang='en', country='us', n_hits=max_count)
        return [result['appId'] for result in results]
    except Exception as e:
        print(f"Arama hatası ({keyword}): {e}")
        return []

if __name__ == "__main__":
    keywords = [
        "action game", "strategy puzzle", "racing simulation", "fitness tracker", "health monitor", "game for kids", 
        "camera app", "music streaming", "video editor", "photo collage", "fitness routine", "travel planner", "budget app", 
        "shopping list", "recipe finder", "travel booking", "hotel reservation", "tax calculator", "loan app", "credit score", 
        "stock tracker", "expense manager", "crypto wallet", "price comparison", "barcode scanner", "event planner", 
        "group chat", "video call", "voice messaging", "social media", "fitness challenge", "language learning", 
        "kids game", "math tutor", "puzzle app", "quiz game", "memory game", "action movie", "funny videos", "DIY tutorial", 
        "learning game", "drawing app", "art maker", "3D design", "digital painting", "sketching app", "coloring book", 
        "photo editing", "video effects", "audio recorder", "soundboard", "text to speech", "document scanner", "file converter", 
        "OCR scanner", "barcode generator", "calendar app", "task organizer", "productivity suite", "focus timer", "time tracker", 
        "reminder app", "meeting scheduler", "note taking", "handwriting app", "todo list", "smart clock", "weather forecast", 
        "alarm clock", "sleep tracker", "breathing exercises", "meditation app", "water reminder", "diet tracker", "step counter", 
        "heart rate monitor", "sleep cycle", "calorie counter", "diet plan", "exercise app", "yoga practice", "running app", 
        "sports tracker", "gym workout", "home workout", "HIIT training", "push-ups tracker", "jump rope app", "bike tracker", 
        "sports news", "live sports", "football scores", "basketball updates", "fitness community", "sports podcast", 
        "music creator", "guitar tuner", "drum kit app", "DJ mixer", "piano lessons", "vocal tuner", "band manager", "karaoke app", 
        "music theory", "song lyrics", "ringtone maker", "music player", "podcast manager", "album art", "sound effects", 
        "video recorder", "live streaming", "video converter", "audio filter", "voice changer", "video slideshow", "sound mixer", 
        "voice assistant", "AI chatbot", "speech to text", "text translation", "language translator", "dictionary app", 
        "grammar checker", "writing assistant", "memo pad", "note editor", "story maker", "ebook reader", "book library", 
        "literature app", "book summary", "reading tracker", "novel reader", "comics reader", "pdf viewer", "ebook downloader", 
        "reading list", "book club", "audio books", "manga collection", "book exchange", "library assistant", "book finder", 
        "book review", "document editor", "PDF editor", "file manager", "cloud storage", "image viewer", "photo storage", 
        "music downloader", "app locker", "password manager", "security app", "file encryption", "VPN service", "private browsing", 
        "firewall app", "antivirus software", "malware scanner", "anti-theft", "privacy protector", "photo vault", "app protector", 
        "privacy settings", "identity theft protection", "spyware removal", "phone tracker", "camera security", "alarm system", 
        "emergency alert", "remote access", "app monitor", "app lock", "private messaging", "encryption tool", "data backup", 
        "memory manager", "RAM booster", "battery saver", "file cleaner", "disk cleaner", "junk file remover", "cache cleaner", 
        "system optimizer", "storage manager", "file shredder", "app manager", "duplicate finder", "task killer", "screen recorder", 
        "app uninstaller", "data recovery", "phone booster", "call blocker", "SMS blocker", "spam filter", "call recorder", 
        "cell phone tracker", "network monitor", "root checker", "compass app", "scanner app", "QR code scanner", "barcodescanner", 
        "trip planner", "car rental", "ride-sharing", "taxis", "bus schedule", "subway map", "directions", "fuel tracker", 
        "driving app", "parking finder", "traffic updates", "route planner", "traffic news", "toll calculator", "gas station finder", 
        "carpool", "flight tracker", "hotel booking", "cruise planner", "restaurant finder", "food delivery", "grocery shopping", 
        "meal prep", "nutrition tracker", "recipe app", "food calories", "diet plan", "cookbook", "local restaurants", 
        "online menu", "food blog", "cooking tutorials", "baking app", "healthy recipes", "wine pairing", "gourmet food", 
        "wine cellar", "cocktail recipes", "barbecue", "grill recipes", "beer guide", "coffee maker", "tea infuser", 
        "smoothie recipes", "breakfast ideas", "international recipes", "tapas", "sushi", "vegan meals", "vegetarian", 
        "keto diet", "paleo diet", "whole food", "gluten free", "superfoods", "weight loss", "protein shakes", "meal tracking", 
        "vegan recipes", "organic food", "dietitian", "food waste", "family meals", "lunch ideas", "healthy snacks", 
        "grocery coupons", "grocery list", "discount coupons", "charity donations", "loyalty program", "gift cards", 
        "public transportation", "transportation network", "rideshare", "bus tracker", "train tracker", "taxi app", "carpooling", 
        "transport maps", "travel guide", "tourist spots", "city guide", "trip journal", "currency converter", "travel deals", 
        "flight bookings", "travel visa", "travel insurance", "vacation app", "holiday planner", "airport map", "travel photos", 
        "travel blog", "food culture", "backpacker", "camping app", "beach resorts", "mountain resorts", "eco tourism", 
        "sustainable travel", "adventure travel", "family travel", "luxury travel", "solo travel", "volunteer travel", 
        "eco-friendly travel", "tourist guides", "travel gear", "backpacking", "photography tips", "local guide", "road trip", 
        "bicycle tour", "sailing tour", "safari app", "luxury hotels", "vacation rentals", "honeymoon destination", "tourist visa", 
        "trip expenses", "adventure activities", "camping gear", "backpacking essentials", "beach vacation", "city breaks", 
        "rural getaway", "train travel", "road trips", "food tours", "museum guides", "national parks", "city tours", "scenic routes",
        "wedding planner", "event photography", "party organizer", "gift finder", "household budget", "personal finance",
        "investment tracker", "home renovation", "pet care", "car maintenance", "tech support", "life hacks", "fashion app",
        "fitness goals", "art app", "home workout", "workout plans", "home cleaning", "job search", "career growth", "entrepreneurship",
        "task manager", "productivity boost", "organization tools", "goal setting", "meditation", "relaxation techniques", 
        "affirmations", "stress relief", "personal coaching", "positive mindset", "digital detox", "sleep aid", "focus music", 
        "mindfulness", "breathing exercises", "mental health", "emotional wellness", "self care", "gratitude journal", "confidence boost",
        "weight loss tracker", "meal planner", "grocery delivery", "exercise routine", "fitness tips", "mental exercises",
        "herbal remedies", "natural healing", "stress management", "dietary supplements", "fitness accessories", "exercise machine",
        "healthy meals", "brain exercises", "memory improvement", "concentration booster", "brain training", "self-improvement",
        "productivity apps", "smart habits", "goal tracker", "time management", "work life balance", "study tools", "learning apps", "meditation", "budgeting", 
        "currency", "wallet", "stocks", "investment","reminder app", "daily planner", "recipe", "meal planner", "shopping list", "habit tracker", "step counter", 
        "keto", "intermittent fasting", "hydration", "mental health", "stress relief", "therapy", "doctor app", "symptom tracker", "heart rate", "sleep cycle", 
        "baby monitor", "parenting", "school planner", "homework", "math games", "chess", "strategy game", "arcade game", "pixel art", "anime", "manga", "drawing pad", 
        "call recorder", "voice changer", "sound effects", "beat maker", "guitar tuner", "piano", "language exchange", "dictionary", "translator", "bible study", 
        "quran", "prayer time", "meditation music", "zen", "virtual pet", "emoji maker", "font keyboard", "wallpaper", "theme", "custom launcher", 
        "file manager", "duplicate cleaner", "battery saver", "ram booster", "vpn proxy", "wifi analyzer", "bluetooth scanner", "QR code", "barcode", 
        "document scanner", "resume builder", "job finder", "freelance", "invoice maker", "tax calculator", "banking", "loan", "credit score", 
        "real estate", "mortgage", "home design", "interior design", "furniture","color palette", "architecture", "3D modeling", "photo editor", 
        "video editor", "slow motion", "GIF maker", "slideshow", "cinema", "series", "drama", "radio", "audiobook", "podcast", "karaoke", 
        "lyrics", "offline music", "offline map", "navigation", "compass", "ride share", "bike rental", "bus tracker", "train schedule", 
        "flight tracker", "boarding pass", "hotel deals", "currency converter", "tip calculator", "weather radar", "hurricane tracker", "earthquake alert", 
        "news aggregator", "sports scores", "football", "basketball", "tennis", "cricket", "fantasy sports", "live streaming", "vlog", "reaction video", 
        "short video", "social media", "photo collage", "filter", "makeup app", "face swap", "aging app", "celebrity lookalike", "couple app", 
        "relationship tracker", "wedding planner", "birthday reminder", "gift ideas", "shopping deals", "price tracker", "discount", 
        "cashback", "barcode scanner", "auction", "car rental", "fuel tracker", "maintenance log", "OBD2", "garage", "motorcycle", "boating", 
        "fishing", "hunting", "camping", "hiking", "navigation tools", "survival guide", "first aid", "emergency alert", "flashlight", "compass tool", 
        "altimeter", "star map", "moon phases", "birdwatching", "plant care", "garden planner", "weather widget", "currency news","daily fitness routine", "healthy meal planner", "guided meditation app", "travel expense tracker",
        "family budget planner", "kids learning game", "photo collage editor", "online shopping list",
        "video editing app", "language learning assistant", "home workout guide", "digital art studio",
        "voice messaging feature", "group chat room", "smart alarm clock", "food recipe finder",
        "recipe calorie calculator", "trip planning assistant", "daily water reminder", "custom workout plan",
        "smart health monitor", "step counter tracker", "guided yoga session", "creative drawing app",
        "coloring book kids", "AI chatbot assistant", "smart photo editor", "live video streaming",
        "funny meme generator", "music streaming app", "kids puzzle game", "math learning tool",
        "document scanner app", "file manager tool", "diet plan tracker", "budget management tool",
        "weather forecast app", "voice assistant feature", "text translation tool", "writing assistant app",
        "video slideshow maker", "digital painting software", "meal prep planner", "event planning tool",
        "personal finance manager", "stock market tracker", "crypto wallet app", "audio recording tool",
        "music player offline", "podcast streaming app", "online radio station", "photo enhancement tool",
        "custom ringtone maker", "language translator tool", "note taking app", "ebook reader app",
        "PDF document scanner", "alarm clock feature", "focus timer tool", "home budget calculator",
        "virtual fitness trainer", "self improvement app", "guided breathing exercises", "daily habit tracker",
        "online education platform", "health tracking app", "fitness challenge mode", "memory improvement game",
        "math puzzle solver", "science learning app", "kids drawing pad", "grammar check tool",
        "currency converter app", "public transport tracker", "flight booking tool", "hotel booking assistant",
        "navigation map app", "road trip planner", "weather alert system", "emergency alert app",
        "voice call recorder", "private photo vault", "phone security app", "file encryption tool",
        "app locker feature", "network usage monitor", "data saving mode", "battery saving app",
        "cache cleaning tool", "duplicate file remover", "QR code scanner", "barcode reader app",
        "remote access tool", "wifi signal booster", "bluetooth device scanner", "screen recording app",
        "system optimization tool", "custom launcher app", "live wallpaper creator", "theme customization tool",
        "smartwatch companion app", "fitness app integration", "photo filter pack", "social media assistant","baby sleep tracker", "language flash cards", "budget savings planner", "mobile banking app",
    "remote learning classroom", "online test creator", "interactive quiz maker", "meal planning app",
    "fitness recipe guide", "guided running coach", "healthy food scanner", "nutrition label reader",
    "pregnancy week tracker", "baby name finder", "medication reminder app", "pill tracking tool",
    "mental health journal", "mood tracking app", "anxiety relief guide", "stress management tool",
    "habit building app", "positive affirmation app", "motivational quotes daily", "focus improvement tool",
    "child education platform", "home schooling support", "toddler learning songs", "drawing lesson app",
    "craft idea generator", "learning activity book", "color theory tutorial", "chess learning app",
    "guitar tuning tool", "piano learning guide", "music composition app", "beat maker studio",
    "voice effects editor", "audiobook player app", "story reading assistant", "vocabulary builder app",
    "spelling practice game", "daily grammar lesson", "math problem solver", "home science experiment",
    "coding tutorial app", "programming practice tool", "online course library", "student planner app",
    "class schedule organizer", "assignment tracking tool", "study motivation quotes", "test prep guide",
    "resume builder app", "job search assistant", "career planning guide", "interview question bank",
    "freelance job finder", "project management tool", "team communication app", "work hours tracker",
    "meeting notes organizer", "presentation maker app", "video conferencing platform", "remote work assistant",
    "office document scanner", "spreadsheet editing tool", "pdf converter app", "calendar event scheduler",
    "reminder notification tool", "to-do list manager", "daily productivity tips", "goal setting journal",
    "time blocking planner", "focus music app", "background noise generator", "white noise machine",
    "mindfulness meditation app", "relaxing sound mixer", "sleep sound creator", "alarm sound changer",
    "screen time tracker", "app usage monitor", "parental control app", "child safety app",
    "location sharing app", "family locator tool", "pet care tracker", "plant watering reminder",
    "grocery shopping planner", "receipt scanner app", "cooking time tracker", "kitchen inventory app",
    "home cleaning schedule", "laundry day planner", "car maintenance log", "fuel consumption tracker",
    "expense splitting app", "group budget tracker", "vacation cost calculator", "shared calendar app",
    "event countdown timer", "birthday reminder tool", "gift idea organizer", "anniversary planner app"
    ]
    seen_apps = set()  # Zaten işlenen App ID'leri tutar
    all_data = []

    for keyword in keywords:
        print(f"Kelime aranıyor: {keyword}")
        app_ids = fetch_top_apps_by_search(keyword)
        
        for app_id in app_ids:
            if app_id not in seen_apps:
                data = get_app_data(app_id)
                if data:
                    all_data.append(data)
                    seen_apps.add(app_id)
                    print(f"Veri alındı: {app_id}")
                time.sleep(0.5)  # Google'a fazla istek göndermemek için bekleme
            else:
                print(f"Zaten işlendi, atlandı: {app_id}")

    # CSV'ye yaz
    df = pd.DataFrame(all_data)
    df.to_csv('google_play_apps_son.csv', index=False)
    print("CSV'ye yazma tamamlandı.")