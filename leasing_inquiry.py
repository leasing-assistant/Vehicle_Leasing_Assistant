import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
import base64

# Helper function to convert image to base64
def get_image_base64(image_path):
    """Convert local image to base64 string for embedding in HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

# Translations
TRANSLATIONS = {
    "English": {
        "page_title": "Vehicle Leasing Assistant",
        "welcome_title": "🚗 Welcome to Your Vehicle Leasing Assistant",
        "welcome_subtitle": "Your trusted partner for vehicle financing solutions",
        "select_category": "🚗 Select Your Vehicle Category",
        "find_plan": "Find Your Perfect Vehicle Leasing Plan",
        "offer_solutions": "We offer flexible leasing solutions for all types of vehicles. Select your vehicle category below to get started with your inquiry.",
        "quick_process": "⚡ Quick Process",
        "quick_process_desc": "Simple and fast inquiry submission process",
        "flexible_terms": "💰 Flexible Terms",
        "flexible_terms_desc": "Competitive rates and flexible tenure options",
        "quick_response": "📞 Quick Response",
        "three_wheeler": "Three Wheeler",
        "car_private": "Car and Private Vehicles",
        "van": "Van",
        "commercial": "Commercial Vehicles",
        "motor_lorry": "Motor Lorry",
        "passenger_bus": "Passenger Bus",
        "select_registration": "Select Registration Status",
        "registered": "Registered",
        "unregistered": "Unregistered",
        "select_type": "Select Vehicle Type",
        "normal": "Normal",
        "luxury": "Luxury",
        "back": "⬅️ Back",
        "vehicle_info": "📅 Vehicle Information",
        "make": "Make *",
        "make_placeholder": "e.g., Toyota, Honda, Nissan",
        "make_help": "Enter the vehicle manufacturer",
        "model": "Model *",
        "model_placeholder": "e.g., Aqua, Vezel, March",
        "model_help": "Enter the vehicle model",
        "vehicle_image": "📷 Vehicle Image",
        "upload_image": "Upload Vehicle Image (Optional)",
        "upload_image_help": "Upload a clear photo of the vehicle",
        "uploaded_image": "Uploaded Vehicle Image",
        "yom": "Year of Manufacture (YOM) *",
        "yom_help": "Select the year your vehicle was manufactured",
        "leasing_details": "💰 Leasing Details",
        "facility_amount": "Expected Facility Amount (LKR) *",
        "facility_help": "Enter the leasing amount you need",
        "tenure": "Tenure (Months) *",
        "tenure_help": "Maximum tenure",
        "timeframe": "Timeframe for Leasing *",
        "timeframe_help": "When do you plan to get the vehicle?",
        "immediately": "Immediately",
        "within_two_days": "Within Two Days",
        "within_one_week": "Within One Week",
        "within_two_weeks": "Within Two Weeks",
        "contact_info": "👤 Contact Information",
        "name": "Full Name *",
        "name_placeholder": "Enter your full name",
        "email": "Email Address",
        "email_placeholder": "your.email@example.com",
        "phone": "Phone Number *",
        "phone_placeholder": "+94 XX XXX XXXX",
        "nearest_town": "Nearest Town *",
        "town_placeholder": "e.g., Colombo, Kandy, Galle",
        "town_help": "Enter your nearest town or city",
        "email_settings": "📧 Email Configuration",
        "sender_email": "Your Email Address",
        "sender_password": "App Password",
        "password_help": "Use Gmail App Password (not regular password)",
        "how_to_create": "How to create App Password:",
        "submit_inquiry": "📤 Submit Inquiry",
        "fill_required": "⚠️ Please fill in all required fields (Name, Phone, Nearest Town)",
        "fill_make_model": "⚠️ Please fill in vehicle make and model",
        "valid_email": "⚠️ Please enter a valid email address (or leave it empty)",
        "configure_email": "⚠️ Please configure email settings in the sidebar first",
        "inquiry_sent": "✅ Inquiry Sent Successfully!",
        "inquiry_failed": "❌ Failed to send inquiry",
        "thank_you": "Thank You for Your Inquiry!",
        "inquiry_submitted": "Your leasing inquiry has been submitted successfully. Our team will review your request and get back to you soon.",
        "inquiry_summary": "📋 Inquiry Summary",
        "vehicle_details": "Vehicle Details:",
        "contact_details": "Contact Details:",
        "leasing_info": "Leasing Information:",
        "back_home": "🏠 Back to Home",
        "language": "Language / භාෂාව"
    },
    "Sinhala": {
        "page_title": "වාහන ලීසිං සහායක",
        "welcome_title": "🚗 ඔබගේ වාහන ලීසිං සහායකයා වෙත සාදරයෙන් පිළිගනිමු",
        "welcome_subtitle": "වාහන මූල්‍ය විසඳුම් සඳහා ඔබගේ විශ්වාසනීය සහකරු",
        "select_category": "🚗 ඔබගේ වාහන වර්ගය තෝරන්න",
        "find_plan": "ඔබගේ පරිපූර්ණ වාහන ලීසිං සැලැස්ම සොයන්න",
        "offer_solutions": "අපි සියලු වර්ගවල වාහන සඳහා නම්‍යශීලී ලීසිං විසඳුම් ලබා දෙමු. ඔබගේ විමසීම ආරම්භ කිරීමට පහත වාහන වර්ගය තෝරන්න.",
        "quick_process": "⚡ ඉක්මන් ක්‍රියාවලිය",
        "quick_process_desc": "සරල හා ඉක්මන් විමසීම් ඉදිරිපත් කිරීමේ ක්‍රියාවලිය",
        "flexible_terms": "💰 නම්‍යශීලී කොන්දේසි",
        "flexible_terms_desc": "තරඟකාරී අනුපාත සහ නම්‍යශීලී කාල සීමා විකල්ප",
        "quick_response": "📞 ඉක්මන් ප්‍රතිචාරය",
        "three_wheeler": "ත්‍රී වීලර්",
        "car_private": "කාර් සහ පුද්ගලික වාහන",
        "van": "වෑන්",
        "commercial": "වාණිජ වාහන",
        "motor_lorry": "ලොරි රථ",
        "passenger_bus": "මගී බස්",
        "select_registration": "ලියාපදිංචි තත්ත්වය තෝරන්න",
        "registered": "ලියාපදිංචි",
        "unregistered": "ලියාපදිංචි නොකළ",
        "select_type": "වාහන වර්ගය තෝරන්න",
        "normal": "සාමාන්‍ය",
        "luxury": "සුඛෝපභෝගී",
        "back": "⬅️ ආපසු",
        "vehicle_info": "📅 වාහන තොරතුරු",
        "make": "නිෂ්පාදකයා *",
        "make_placeholder": "උදා: Toyota, Honda, Nissan",
        "make_help": "වාහන නිෂ්පාදකයා ඇතුළත් කරන්න",
        "model": "මාදිලිය *",
        "model_placeholder": "උදා: Aqua, Vezel, March",
        "model_help": "වාහන මාදිලිය ඇතුළත් කරන්න",
        "vehicle_image": "📷 වාහන රූපය",
        "upload_image": "වාහන රූපය උඩුගත කරන්න (විකල්ප)",
        "upload_image_help": "වාහනයේ පැහැදිලි ඡායාරූපයක් උඩුගත කරන්න",
        "uploaded_image": "උඩුගත කළ වාහන රූපය",
        "yom": "නිෂ්පාදන වර්ෂය (YOM) *",
        "yom_help": "ඔබේ වාහනය නිෂ්පාදනය කළ වර්ෂය තෝරන්න",
        "leasing_details": "💰 ලීසිං විස්තර",
        "facility_amount": "අපේක්ෂිත පහසුකම් මුදල (රු.) *",
        "facility_help": "ඔබට අවශ්‍ය ලීසිං මුදල ඇතුළත් කරන්න",
        "tenure": "කාලසීමාව (මාස) *",
        "tenure_help": "උපරිම කාලසීමාව",
        "timeframe": "ලීසිං සඳහා කාල රාමුව *",
        "timeframe_help": "ඔබ වාහනය ලබා ගැනීමට සැලසුම් කරන්නේ කවදාද?",
        "immediately": "වහාම",
        "within_two_days": "දින දෙකක් ඇතුළත",
        "within_one_week": "සතියක් ඇතුළත",
        "within_two_weeks": "සති දෙකක් ඇතුළත",
        "contact_info": "👤 සම්බන්ධතා තොරතුරු",
        "name": "සම්පූර්ණ නම *",
        "name_placeholder": "ඔබගේ සම්පූර්ණ නම ඇතුළත් කරන්න",
        "email": "විද්‍යුත් තැපැල් ලිපිනය",
        "email_placeholder": "your.email@example.com",
        "phone": "දුරකථන අංකය *",
        "phone_placeholder": "+94 XX XXX XXXX",
        "nearest_town": "ආසන්නතම නගරය *",
        "town_placeholder": "උදා: කොළඹ, මහනුවර, ගාල්ල",
        "town_help": "ඔබගේ ආසන්නතම නගරය හෝ නගරය ඇතුළත් කරන්න",
        "email_settings": "📧 විද්‍යුත් තැපැල් වින්‍යාසය",
        "sender_email": "ඔබගේ විද්‍යුත් තැපැල් ලිපිනය",
        "sender_password": "යෙදුම් මුරපදය",
        "password_help": "Gmail යෙදුම් මුරපදය භාවිතා කරන්න (සාමාන්‍ය මුරපදය නොවේ)",
        "how_to_create": "යෙදුම් මුරපදය සෑදීමේ ක්‍රමය:",
        "submit_inquiry": "📤 විමසීම ඉදිරිපත් කරන්න",
        "fill_required": "⚠️ කරුණාකර සියලුම අවශ්‍ය ක්ෂේත්‍ර පුරවන්න (නම, දුරකථනය, ආසන්නතම නගරය)",
        "fill_make_model": "⚠️ කරුණාකර වාහන නිෂ්පාදකයා සහ මාදිලිය පුරවන්න",
        "valid_email": "⚠️ කරුණාකර වලංගු විද්‍යුත් තැපැල් ලිපිනයක් ඇතුළත් කරන්න (හෝ එය හිස්ව තබන්න)",
        "configure_email": "⚠️ කරුණාකර පළමුව පැති තීරුවේ විද්‍යුත් තැපැල් සැකසුම් වින්‍යාස කරන්න",
        "inquiry_sent": "✅ විමසීම සාර්ථකව යවන ලදී!",
        "inquiry_failed": "❌ විමසීම යැවීමට අසමත් විය",
        "thank_you": "ඔබගේ විමසීමට ස්තූතියි!",
        "inquiry_submitted": "ඔබගේ ලීසිං විමසීම සාර්ථකව ඉදිරිපත් කර ඇත. අපගේ කණ්ඩායම ඔබගේ ඉල්ලීම සමාලෝචනය කර ඉක්මනින් ඔබ වෙත පැමිණෙනු ඇත.",
        "inquiry_summary": "📋 විමසීම් සාරාංශය",
        "vehicle_details": "වාහන විස්තර:",
        "contact_details": "සම්බන්ධතා විස්තර:",
        "leasing_info": "ලීසිං තොරතුරු:",
        "back_home": "🏠 මුල් පිටුවට ආපසු",
        "language": "Language / භාෂාව"
    }
}

# Page configuration
st.set_page_config(
    page_title="Vehicle Leasing Assistant",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive styling with FIXED TEXT VISIBILITY
st.markdown("""
    <style>
    /* Force all text to be dark and visible on light background */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.95)),
                    url('https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=1920&h=1080&fit=crop') no-repeat center center fixed;
        background-size: cover;
        color: #2c3e50 !important;
    }
    
    /* Override all Streamlit text elements to be dark */
    .stApp * {
        color: #2c3e50 !important;
    }
    
    /* Specific overrides for common elements */
    p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: #2c3e50 !important;
    }
    
    /* Input labels and text */
    .stTextInput label, .stNumberInput label, .stSelectbox label, 
    .stSlider label, .stFileUploader label {
        color: #2c3e50 !important;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        color: #2c3e50 !important;
        background-color: white !important;
    }
    
    /* Markdown text */
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: #2c3e50 !important;
    }
    
    .big-font {
        font-size: 50px !important;
        font-weight: bold;
        color: #2c3e50 !important;
        text-align: center;
        margin-bottom: 30px;
    }
    .subtitle {
        font-size: 20px;
        color: #34495e !important;
        text-align: center;
        margin-bottom: 40px;
    }
    .stButton>button {
        width: 100%;
        background: #2c3e50 !important;
        color: white !important;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 15px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #34495e !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .info-box {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        color: #2c3e50 !important;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .info-box * {
        color: #2c3e50 !important;
    }
    .success-box {
        background: #d4edda;
        border: 2px solid #c3e6cb;
        color: #155724 !important;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .success-box * {
        color: #155724 !important;
    }
    
    /* Sidebar text */
    .css-1d391kg, [data-testid="stSidebar"] {
        color: #2c3e50 !important;
    }
    [data-testid="stSidebar"] * {
        color: #2c3e50 !important;
    }
    
    /* Metric labels and values */
    .stMetric label, .stMetric div {
        color: #2c3e50 !important;
    }
    
    /* Info, success, error boxes */
    .stAlert {
        color: #2c3e50 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Language selector in sidebar
with st.sidebar:
    st.markdown(f"### {TRANSLATIONS[st.session_state.language]['language']}")
    selected_language = st.selectbox(
        "Select Language",
        ["English", "Sinhala"],
        index=0 if st.session_state.language == "English" else 1,
        key="language_selector",
        label_visibility="collapsed"
    )
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()

# Get current translations
t = TRANSLATIONS[st.session_state.language]

# Vehicle categories with icons
VEHICLE_CATEGORIES = {
    "🛺 Three Wheeler": {
        "icon": "🛺",
        "name": "Three Wheeler",
        "max_tenure": 60,
        "has_subcategory": False,
        "image": "threewheeler.png"
    },
    "🚗 Car and Private Vehicles": {
        "icon": "🚗",
        "name": "Car and Private Vehicles",
        "max_tenure": 84,
        "has_subcategory": True,
        "image": "personal1.png",
        "subcategories": {
            "Registered": {
                "types": ["Normal", "Luxury"]
            },
            "Unregistered": {
                "types": ["Normal", "Luxury"]
            }
        }
    },
    "🚐 Van": {
        "icon": "🚐",
        "name": "Van",
        "max_tenure": 72,
        "has_subcategory": True,
        "image": "van.png",
        "subcategories": {
            "Registered": {
                "types": ["Normal", "Luxury"]
            },
            "Unregistered": {
                "types": ["Normal", "Luxury"]
            }
        }
    },
    "🚙 Commercial Vehicles": {
        "icon": "🚙",
        "name": "Commercial Vehicles",
        "max_tenure": 72,
        "has_subcategory": True,
        "image": "commercial1.png",
        "subcategories": {
            "Registered": {
                "types": ["Normal", "Luxury"]
            },
            "Unregistered": {
                "types": ["Normal", "Luxury"]
            }
        }
    },
    "🚚 Motor Lorry": {
        "icon": "🚚",
        "name": "Motor Lorry",
        "max_tenure": 60,
        "has_subcategory": True,
        "image": "lorry.png",
        "subcategories": {
            "Registered": {
                "types": ["Normal", "Luxury"]
            },
            "Unregistered": {
                "types": ["Normal", "Luxury"]
            }
        }
    },
    "🚌 Passenger Bus": {
        "icon": "🚌",
        "name": "Passenger Bus",
        "max_tenure": 60,
        "has_subcategory": True,
        "image": "bus.png",
        "subcategories": {
            "Registered": {
                "types": ["Normal", "Luxury"]
            },
            "Unregistered": {
                "types": ["Normal", "Luxury"]
            }
        }
    }
}

def send_inquiry_email(customer_name, customer_email, customer_phone, vehicle_info, vehicle_year, 
                       facility_amount, tenure_months, nearest_town, timeframe, sender_email, sender_password,
                       vehicle_make=None, vehicle_model=None, registration_status=None, vehicle_type=None,
                       vehicle_image=None):
    """Send inquiry email to banker using Gmail SMTP"""
    banker_email = "keshara@sdb.lk"
    
    subject = f"Vehicle Leasing Inquiry - {vehicle_info['name']}"
    
    # Build vehicle details section
    vehicle_details = f"- Category: {vehicle_info['name']}"
    if registration_status:
        vehicle_details += f"\n- Registration Status: {registration_status}"
    if vehicle_type:
        vehicle_details += f"\n- Vehicle Type: {vehicle_type}"
    if vehicle_make:
        vehicle_details += f"\n- Make: {vehicle_make}"
    if vehicle_model:
        vehicle_details += f"\n- Model: {vehicle_model}"
    vehicle_details += f"\n- Year of Manufacture (YOM): {vehicle_year}"
    
    body = f"""
New Vehicle Leasing Inquiry

Customer Information:
- Name: {customer_name}
- Email: {customer_email}
- Phone: {customer_phone}
- Nearest Town: {nearest_town}

Vehicle Details:
{vehicle_details}
- Expected Facility Amount: LKR {facility_amount:,.2f}
- Requested Tenure: {tenure_months} months ({tenure_months/12:.1f} years)
- When Customer Needs Leasing: {timeframe}
{"- Vehicle Image: Attached" if vehicle_image else ""}

Please contact the customer to discuss leasing options.

Date of Inquiry: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = banker_email
        msg['Subject'] = subject
        msg['Reply-To'] = customer_email
        
        # Attach body
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach vehicle image if provided
        if vehicle_image is not None:
            try:
                # Read the uploaded file
                image_data = vehicle_image.read()
                image_name = vehicle_image.name
                
                # Create image attachment
                image_part = MIMEImage(image_data, name=image_name)
                image_part.add_header('Content-Disposition', f'attachment; filename="{image_name}"')
                msg.attach(image_part)
            except Exception as img_error:
                print(f"Error attaching image: {img_error}")
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return True, banker_email, subject, body
    except Exception as e:
        return False, banker_email, subject, body, str(e)

def show_welcome_page():
    """Display the welcome/landing page"""
    st.markdown(f'<p class="big-font">{t["welcome_title"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{t["welcome_subtitle"]}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Welcome message
    st.markdown(f"""
        <div class="info-box">
            <h3 style="text-align: center;">{t["find_plan"]}</h3>
            <p style="text-align: center; font-size: 18px;">
                {t["offer_solutions"]}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### {t['select_category']}")
    st.markdown("")
    
    # Display vehicle categories with images in a grid
    col1, col2, col3 = st.columns(3)
    
    categories_list = list(VEHICLE_CATEGORIES.keys())
    
    for idx, category in enumerate(categories_list):
        col_idx = idx % 3
        if col_idx == 0:
            current_col = col1
        elif col_idx == 1:
            current_col = col2
        else:
            current_col = col3
        
        with current_col:
            vehicle_info = VEHICLE_CATEGORIES[category]
            
            # Display vehicle image
            image_path = vehicle_info['image']
            image_base64 = get_image_base64(image_path)
            
            if image_base64:
                st.markdown(f"""
                    <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px;">
                        <img src="data:image/png;base64,{image_base64}" style="width: 100%; height: 200px; object-fit: cover;">
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Fallback if image doesn't load
                st.markdown(f"""
                    <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; background: #f0f0f0; height: 200px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 48px;">{vehicle_info['icon']}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            # Button for category selection
            # Get translated name based on vehicle type
            vehicle_name = vehicle_info['name']
            if vehicle_name == "Three Wheeler":
                translated_name = t['three_wheeler']
            elif vehicle_name == "Car and Private Vehicles":
                translated_name = t['car_private']
            elif vehicle_name == "Van":
                translated_name = t['van']
            elif vehicle_name == "Commercial Vehicles":
                translated_name = t['commercial']
            elif vehicle_name == "Motor Lorry":
                translated_name = t['motor_lorry']
            elif vehicle_name == "Passenger Bus":
                translated_name = t['passenger_bus']
            else:
                translated_name = vehicle_name
            
            if st.button(f"{vehicle_info['icon']} {translated_name}", key=f"btn_{category}", use_container_width=True):
                st.session_state.selected_category = category
                if vehicle_info['has_subcategory']:
                    st.session_state.page = "subcategory"
                else:
                    st.session_state.page = "inquiry"
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Additional information
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="info-box">
                <h4>{t["quick_process"]}</h4>
                <p>{t["quick_process_desc"]}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="info-box">
                <h4>{t["flexible_terms"]}</h4>
                <p>{t["flexible_terms_desc"]}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="info-box">
                <h4>{t["quick_response"]}</h4>
                <p>Udara Keshara : 075-429 0022</p>
            </div>
        """, unsafe_allow_html=True)

def show_subcategory_page():
    """Display subcategory selection page for private vehicles"""
    category = st.session_state.selected_category
    vehicle_info = VEHICLE_CATEGORIES[category]
    
    # Back button
    if st.button(t["back"], key="back_sub"):
        st.session_state.page = "welcome"
        st.rerun()
    
    # Get translated vehicle name
    vehicle_name = vehicle_info['name']
    if vehicle_name == "Three Wheeler":
        translated_name = t['three_wheeler']
    elif vehicle_name == "Car and Private Vehicles":
        translated_name = t['car_private']
    elif vehicle_name == "Van":
        translated_name = t['van']
    elif vehicle_name == "Commercial Vehicles":
        translated_name = t['commercial']
    elif vehicle_name == "Motor Lorry":
        translated_name = t['motor_lorry']
    elif vehicle_name == "Passenger Bus":
        translated_name = t['passenger_bus']
    else:
        translated_name = vehicle_name
    
    st.markdown(f'<p class="big-font">{vehicle_info["icon"]} {translated_name}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{t["select_registration"]}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 1: Registration Status
    st.markdown(f"### 📋 {t['select_registration']}")
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"📝\n\n{t['registered']}\n\n", key="registered", use_container_width=True):
            st.session_state.registration_status = "Registered"
            st.session_state.show_vehicle_type = True
            st.rerun()
    
    with col2:
        if st.button(f"📄\n\n{t['unregistered']}\n\n", key="unregistered", use_container_width=True):
            st.session_state.registration_status = "Unregistered"
            st.session_state.show_vehicle_type = True
            st.rerun()
    
    # Step 2: Vehicle Type (shown after registration status is selected)
    if 'show_vehicle_type' in st.session_state and st.session_state.show_vehicle_type:
        st.markdown("---")
        reg_status = t['registered'] if st.session_state.registration_status == "Registered" else t['unregistered']
        st.markdown(f"### 🚗 {t['select_type']} ({reg_status})")
        st.markdown("")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"🚙\n\n{t['normal']}\n\n", key="normal", use_container_width=True):
                st.session_state.vehicle_type = "Normal"
                st.session_state.page = "inquiry"
                st.rerun()
        
        with col2:
            if st.button(f"💎\n\n{t['luxury']}\n\n", key="luxury", use_container_width=True):
                st.session_state.vehicle_type = "Luxury"
                st.session_state.page = "inquiry"
                st.rerun()

def show_inquiry_page(sender_email, sender_password):
    """Display the inquiry form page"""
    category = st.session_state.selected_category
    vehicle_info = VEHICLE_CATEGORIES[category]
    
    # Back button
    back_page = "subcategory" if vehicle_info.get('has_subcategory', False) else "welcome"
    if st.button(t["back"], key="back"):
        st.session_state.page = back_page
        st.rerun()
    
    # Get translated vehicle name
    vehicle_name = vehicle_info['name']
    if vehicle_name == "Three Wheeler":
        translated_name = t['three_wheeler']
    elif vehicle_name == "Car and Private Vehicles":
        translated_name = t['car_private']
    elif vehicle_name == "Van":
        translated_name = t['van']
    elif vehicle_name == "Commercial Vehicles":
        translated_name = t['commercial']
    elif vehicle_name == "Motor Lorry":
        translated_name = t['motor_lorry']
    elif vehicle_name == "Passenger Bus":
        translated_name = t['passenger_bus']
    else:
        translated_name = vehicle_name
    
    # Build title with subcategory info if applicable
    title = f'{vehicle_info["icon"]} {translated_name}'
    if 'registration_status' in st.session_state:
        reg_stat = t['registered'] if st.session_state.registration_status == "Registered" else t['unregistered']
        veh_type = t['normal'] if st.session_state.vehicle_type == "Normal" else t['luxury']
        title += f' - {reg_stat} ({veh_type})'
    
    st.markdown(f'<p class="big-font">{title}</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Fill in your details to submit your leasing inquiry</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Vehicle Details Section
    st.markdown("### 📋 Vehicle & Leasing Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {t['vehicle_info']}")
        
        # Only show make and model for non-Three Wheeler vehicles
        if "Three Wheeler" not in vehicle_info['name']:
            vehicle_make = st.text_input(
                t['make'],
                placeholder=t['make_placeholder'],
                help=t['make_help']
            )
            
            vehicle_model = st.text_input(
                t['model'],
                placeholder=t['model_placeholder'],
                help=t['model_help']
            )
            
            st.markdown(f"#### {t['vehicle_image']}")
            vehicle_image = st.file_uploader(
                t['upload_image'],
                type=["jpg", "jpeg", "png"],
                help=t['upload_image_help']
            )
            
            if vehicle_image is not None:
                st.image(vehicle_image, caption=t['uploaded_image'], use_column_width=True)
        else:
            # Three Wheeler - no make/model fields
            vehicle_make = None
            vehicle_model = None
            vehicle_image = None
        
        current_year = datetime.now().year
        vehicle_year = st.selectbox(
            t['yom'],
            options=list(range(current_year, current_year - 20, -1)),
            help=t['yom_help']
        )
        
        vehicle_age = current_year - vehicle_year
        st.info(f"Vehicle Age: **{vehicle_age} years**")
        
        st.markdown(f"#### {t['leasing_details']}")
        facility_amount = st.number_input(
            t['facility_amount'],
            min_value=100000,
            max_value=50000000,
            value=1000000,
            step=50000,
            help=t['facility_help']
        )
        
        st.metric(t['facility_amount'].replace(' *', ''), f"LKR {facility_amount:,.2f}")
    
    with col2:
        st.markdown(f"#### {t['tenure']}")
        max_tenure = vehicle_info['max_tenure']
        
        tenure_months = st.slider(
            t['tenure'],
            min_value=12,
            max_value=max_tenure,
            value=36,
            step=6,
            help=f"{t['tenure_help']}: {max_tenure} months"
        )
        
        tenure_years = tenure_months / 12
        st.info(f"{t['tenure'].replace(' *', '')}: **{tenure_years:.1f} years** ({tenure_months} months)")
        
        st.markdown(f"#### {t['timeframe']}")
        timeframe_options = [
            t['immediately'],
            t['within_two_days'],
            t['within_one_week'],
            t['within_two_weeks']
        ]
        timeframe = st.selectbox(
            t['timeframe'],
            options=timeframe_options,
            help=t['timeframe_help']
        )
    
    # Customer Information Section
    st.markdown("---")
    st.markdown(f"### {t['contact_info']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        customer_name = st.text_input(
            t['name'],
            placeholder=t['name_placeholder'],
            help=t.get('name_help', '')
        )
        
        customer_email = st.text_input(
            t['email'],
            placeholder=t['email_placeholder'],
            help=t.get('email_help', '')
        )
    
    with col2:
        customer_phone = st.text_input(
            t['phone'],
            placeholder=t['phone_placeholder'],
            help=t.get('phone_help', '')
        )
        
        nearest_town = st.text_input(
            t['nearest_town'],
            placeholder=t['town_placeholder'],
            help=t['town_help']
        )
    
    # Submit Inquiry button
    st.markdown("---")
    if st.button(t['submit_inquiry'], key="submit", use_container_width=True):
        # Validate inputs
        if not customer_name or not customer_phone or not nearest_town:
            st.error(t['fill_required'])
        elif "Three Wheeler" not in vehicle_info['name'] and (not vehicle_make or not vehicle_model):
            st.error(t['fill_make_model'])
        elif customer_email and ("@" not in customer_email or "." not in customer_email):
            st.error(t['valid_email'])
        elif not sender_email or not sender_password:
            st.error(t['configure_email'])
        else:
            # Get subcategory info if available
            registration_status = st.session_state.get('registration_status', None)
            vehicle_type = st.session_state.get('vehicle_type', None)
            
            # Show sending message
            with st.spinner("Sending inquiry email..."):
                # Send email
                result = send_inquiry_email(
                    customer_name,
                    customer_email,
                    customer_phone,
                    vehicle_info,
                    vehicle_year,
                    facility_amount,
                    tenure_months,
                    nearest_town,
                    timeframe,
                    sender_email,
                    sender_password,
                    vehicle_make,
                    vehicle_model,
                    registration_status,
                    vehicle_type,
                    vehicle_image
                )
            
            if result[0]:  # Success
                banker_email, subject, body = result[1], result[2], result[3]
                
                # Store inquiry data in session state
                vehicle_full_name = vehicle_info['name']
                if registration_status:
                    vehicle_full_name += f" - {registration_status} ({vehicle_type})"
                
                st.session_state.inquiry_data = {
                    'vehicle_name': vehicle_full_name,
                    'vehicle_make': vehicle_make,
                    'vehicle_model': vehicle_model,
                    'vehicle_year': vehicle_year,
                    'facility_amount': facility_amount,
                    'tenure_months': tenure_months,
                    'tenure_years': tenure_years,
                    'timeframe': timeframe,
                    'customer_name': customer_name,
                    'customer_email': customer_email,
                    'customer_phone': customer_phone,
                    'nearest_town': nearest_town,
                    'email_body': body,
                    'banker_email': banker_email,
                    'has_image': vehicle_image is not None
                }
                
                # Redirect to thank you page
                st.session_state.page = "thankyou"
                st.rerun()
            else:  # Failed
                banker_email, subject, body, error = result[1], result[2], result[3], result[4]
                
                st.error(f"❌ Failed to send email: {error}")
                st.warning("""
                **Troubleshooting Tips:**
                - Make sure you're using a Gmail App Password, not your regular password
                - Enable 2-Step Verification in your Google Account
                - Generate an App Password from: https://myaccount.google.com/apppasswords
                - Check your internet connection
                """)

def show_thank_you_page():
    """Display the thank you page after successful submission"""
    st.markdown(f'<p class="big-font">✅ {t["thank_you"]}</p>', unsafe_allow_html=True)
    
    # Centered message
    st.markdown(f"""
        <div style="text-align: center; margin: 40px 0;">
            <h2 style="color: #2c3e50;">📧 {t["inquiry_submitted"]}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display inquiry summary from session state
    if 'inquiry_data' in st.session_state:
        data = st.session_state.inquiry_data
        
        st.markdown(f"### {t['inquiry_summary']}")
        
        # Build vehicle details with conditional make/model
        vehicle_details_html = f"""
            <div class="info-box">
                <h4>{t['vehicle_details']}</h4>
                <ul>
                    <li><strong>{t.get('vehicle_info', 'Category').replace('🗓️ ', '').replace(' *', '')}:</strong> {data['vehicle_name']}</li>"""
        
        if 'vehicle_make' in data and data['vehicle_make']:
            vehicle_details_html += f"""<li><strong>{t['make'].replace(' *', '')}:</strong> {data['vehicle_make']}</li>"""
        if 'vehicle_model' in data and data['vehicle_model']:
            vehicle_details_html += f"""<li><strong>{t['model'].replace(' *', '')}:</strong> {data['vehicle_model']}</li>"""
        
        vehicle_details_html += f"""
                    <li><strong>{t['yom'].replace(' *', '')}:</strong> {data['vehicle_year']}</li>
                    <li><strong>{t['facility_amount'].replace(' *', '')}:</strong> LKR {data['facility_amount']:,.2f}</li>
                    <li><strong>{t['tenure'].replace(' *', '')}:</strong> {data['tenure_months']} months ({data['tenure_years']:.1f} years)</li>
                    <li><strong>{t['timeframe'].replace(' *', '')}:</strong> {data['timeframe']}</li>"""
        
        if data.get('has_image', False):
            vehicle_details_html += f"""<li><strong>{t['vehicle_image'].replace('📷 ', '')}:</strong> ✅ Attached to email</li>"""
        
        vehicle_details_html += """</ul>"""
        
        st.markdown(vehicle_details_html + f"""
                <h4 style="margin-top: 20px;">{t['contact_details']}</h4>
                <ul>
                    <li><strong>{t['name'].replace(' *', '')}:</strong> {data['customer_name']}</li>
                    <li><strong>{t['email']}:</strong> {data['customer_email']}</li>
                    <li><strong>{t['phone'].replace(' *', '')}:</strong> {data['customer_phone']}</li>
                    <li><strong>{t['nearest_town'].replace(' *', '')}:</strong> {data['nearest_town']}</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # Show email details for reference
        with st.expander("📄 View Email Details"):
            st.text_area("Email Content", data['email_body'], height=400, disabled=True)
            st.info(f"This inquiry was sent to: **{data['banker_email']}**")
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Submit Another Inquiry", key="new_inquiry", use_container_width=True):
            st.session_state.page = "welcome"
            if 'selected_category' in st.session_state:
                del st.session_state.selected_category
            if 'inquiry_data' in st.session_state:
                del st.session_state.inquiry_data
            st.rerun()
    with col2:
        if st.button(t["back_home"], key="home_final", use_container_width=True):
            st.session_state.page = "welcome"
            if 'selected_category' in st.session_state:
                del st.session_state.selected_category
            if 'inquiry_data' in st.session_state:
                del st.session_state.inquiry_data
            st.rerun()

def main():
    """Main application function"""
    # Load environment variables
    load_dotenv()
    SENDER_EMAIL = os.getenv("EMAIL")
    SENDER_PASSWORD = os.getenv("PASSWORD")

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "welcome"
    
    # Route to appropriate page
    if st.session_state.page == "welcome":
        show_welcome_page()
    elif st.session_state.page == "subcategory":
        show_subcategory_page()
    elif st.session_state.page == "inquiry":
        show_inquiry_page(SENDER_EMAIL, SENDER_PASSWORD)
    elif st.session_state.page == "thankyou":
        show_thank_you_page()

if __name__ == "__main__":
    main()
