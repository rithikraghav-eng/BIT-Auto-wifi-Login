import requests
import time

session = requests.Session()

# -------------------------------
# BIT Portal URLs
# -------------------------------
delete_auth_url = "http://172.16.0.200:2280/cportal/ip/del_old_session_by_auth.php"
final_delete_url = "http://172.16.0.200:2280/submit/del_old_user_session.php"
login_url = "http://172.16.0.200:2280/submit/user_login.php"

# -------------------------------
# Your credentials
# -------------------------------
username = "usrnm"
password = "pswd"

# Step 1 – Delete old session
def delete_old_session():
    try:
        print(" Step 1: Deleting old session (auth)...")
        r1 = session.get(delete_auth_url, timeout=5)
        if r1.status_code == 200:
            print(" Auth deletion page loaded.")
        else:
            print(f" Auth page returned {r1.status_code}")

        # Now submit the hidden form with pcomp/hotspot/user credentials
        print(" Step 2: Completing old session deletion...")
        data = {
            "pcomp": "hotspot",
            "usrname": username,
            "newpasswd": password,
        }
        r2 = session.post(final_delete_url, data=data, timeout=5)
        if "Deleted" in r2.text or "Go to Login Page" in r2.text:
            print(" Old session deleted successfully!")
            return True
        else:
            print(" Could not confirm deletion. Response preview:")
            print(r2.text[:200])
            return False
    except Exception as e:
        print(" Error while deleting old session:", e)
        return False

# Step 3 – Login again
def login():
    try:
        print(" Step 3: Logging in to BIT Wi-Fi...")
        payload = {
            "usrname": username,
            "newpasswd": password,
            "terms": "on",
            "page_sid": "internal",
            "org_url": "http://connectivitycheck.gstatic.com/generate_204"
        }
        r = session.post(login_url, data=payload, timeout=5)
        if any(k in r.text.lower() for k in ["logout", "connected", "portal_logout", "success"]):
            print(" Logged in successfully!")
        elif "concurrent logins exceeded" in r.text.lower():
            print(" Still hitting concurrent login issue — might need another delete attempt.")
        else:
            print(" Login may have failed. Response snippet:")
            print(r.text[:300])
    except Exception as e:
        print(" Error during login:", e)

def main():
    print(" BIT Auto Old-Session Cleaner + Auto-Login\n")
    if delete_old_session():
        time.sleep(2)
        login()
    else:
        print(" Skipping login because old session could not be deleted.")

if __name__ == "__main__":

    main()
