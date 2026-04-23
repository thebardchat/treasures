import firebase_admin
from firebase_admin import credentials, firestore
import gspread

# --- CONFIGURATION ---
CREDENTIALS_PATH = "credentials.json"
SHEET_ID = "12a3qigHIgTuPwmzZFJ27GvGO2Yslv6ObNz-mjQFQCDo"
APP_ID = "logibot"

# 1. INITIALIZE FIREBASE (The Database)
if not firebase_admin._apps:
    cred = credentials.Certificate(CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
db = firestore.client()
print("✅ Firebase initialized.")

# 2. INITIALIZE GOOGLE SHEETS (The Source)
gc = gspread.service_account(filename=CREDENTIALS_PATH)
sh = gc.open_by_key(SHEET_ID)
print("✅ Google Sheets connected.")

def sync_tab(tab_name, collection_name):
    print(f"\n--- Syncing {tab_name} ---")
    try:
        worksheet = sh.worksheet(tab_name)
        data = worksheet.get_all_records()
        
        # Collection Reference: artifacts/logibot/public/data/{collection_name}
        collection_ref = db.collection(f"artifacts/{APP_ID}/public/data/{collection_name}")
        
        # Batch write for speed
        batch = db.batch()
        count = 0
        
        for row in data:
            # Create a unique ID based on the first column (e.g., Member Name or Goal Name)
            # We filter out empty rows just in case
            if not row: continue
            
            first_key = list(row.keys())[0]
            doc_id = str(row[first_key]).replace("/", "-").strip()
            
            if doc_id:
                doc_ref = collection_ref.document(doc_id)
                batch.set(doc_ref, row)
                count += 1
        
        batch.commit()
        print(f"✅ Successfully synced {count} items to '{collection_name}'.")
        
    except gspread.WorksheetNotFound:
        print(f"⚠️ Warning: Tab '{tab_name}' not found. Skipping.")
    except Exception as e:
        print(f"❌ Error syncing {tab_name}: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Sync the 3 Life Tabs
    sync_tab("Family_Intel", "family")
    sync_tab("Finance_Overview", "finance")
    sync_tab("Strategic_Goals", "goals")
    
    print("\n🎉 Life Sync Complete. The AI now knows your context.")