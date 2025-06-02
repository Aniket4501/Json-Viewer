import streamlit as st
import json
import pandas as pd
from typing import Dict, List, Any
import io
import base64

# Page configuration
st.set_page_config(
    page_title="JSON Test Case Editor",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Default test case template
DEFAULT_TEST_CASE = {
    "mhm": {
        "age": 25, "hgt": 185, "wgt": 77, "sex": 1, "dbp": 78, "map": 85, "sbp": 118,
        "fat": 20, "ppr": 40, "rhr": 70, "rhr_day": [70], "spo2": 99, "vo2max": 59.5,
        "whr": 0.8, "wst": 80, "alc": 80, "cst": 80, "exh": 80, "fCV": 80, "fDM": 80,
        "fMI": 80, "pHT": 80, "a1c": 80, "acr": 80, "cre": 80, "crp": 80, "cys": 80,
        "fbg": 80, "eag": 80, "gfr": 80, "hdl": 80, "ldl": 80, "tgl": 80, "tsc": 80,
        "vdl": 80, "CAN": 0, "CHD": 0, "CHF": 0, "CKD": 0, "CVD": 0, "DM2": 1,
        "HTN": 0, "LDS": 0, "LVH": 0, "PDM": 0, "PMI": 0, "STK": 0, "TDM": 0, "THT": 0
    },
    "smk": {"now": 0, "evr": 0, "yrs": 0, "num": 0, "qit": 0, "slt": 0},
    "slp": {"bed": [8.5], "slp": [8.0], "awk": [1], "slp_avg": [8]},
    "nut": {
        "nqs01": 0.5, "nqs02": 0.5, "nqs03": 0.5, "nqs04": 0.5, "nqs05": 0.5,
        "nqs06": 0.5, "nqs07": 0.5, "nqs08": 0.5, "nqs09": 0.5, "nqs10": 0.5,
        "nqs11": 0.5, "nqs12": 0.5, "nqs13": 0.5, "nqs14": 0.5, "nqs15": 0.5,
        "nqs16": 0.5, "nqs17": 0.5, "nqs18": 0.5, "nqs19": 0.5, "nqs20": 0.5,
        "nqs21": 0.5, "nqs22": 0.5, "protein": 0.5, "sfat": 0.5, "sugar": 0.5,
        "fiber": 0.5, "sodium": 0.5, "vitamin_c": 0.5, "iron": 0.5,
        "percentage_drink": 0.5, "density_drink": 0.5
    },
    "qlm": {
        "q01": 0.5, "q02": 0.5, "q03": 0.5, "q04": 0.5, "q05": 0.5, "q06": 0.5,
        "q07": 0.5, "q08": 0.5, "q09": 0.5, "q10": 0.5, "q11": 0.5, "q12": 0.5,
        "q13": 0.5, "q14": 0.5, "q15": 0.5, "q16": 0.5, "q17": 0.5, "q18": 0.5,
        "q19": 0.5, "q20": 0.5, "q21": 0.5, "q22": 0.5, "q23": 0.5, "q24": 0.5,
        "q25": 0.5, "q26": 0.5, "q27": 0.5, "gad01": 0.5, "gad02": 0.5, "gad03": 0.5,
        "gad04": 0.5, "gad05": 0.5, "gad06": 0.5, "gad07": 0.5, "phq01": 0.5,
        "phq02": 0.5, "phq03": 0.5, "phq04": 0.5, "phq05": 0.5, "phq06": 0.5,
        "phq07": 0.5, "phq08": 0.5, "phq09": 0.5, "pss01": 0.5, "pss02": 0.5,
        "pss03": 0.5, "pss04": 0.5, "pss05": 0.5, "pss06": 0.5, "pss07": 0.5,
        "pss08": 0.5, "pss09": 0.5, "pss10": 0.5, "gsrh": 0.5, "maas01": 0.5,
        "maas02": 0.5, "maas03": 0.5, "maas04": 0.5, "maas05": 0.5, "maas06": 0.5,
        "maas07": 0.5, "maas08": 0.5, "maas09": 0.5, "maas10": 0.5, "maas11": 0.5,
        "maas12": 0.5, "maas13": 0.5, "maas14": 0.5, "maas15": 0.5, "mfm": [0.5]
    },
    "clip": False
}

# Initialize session state
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []
if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None

def validate_json(json_string: str) -> tuple[bool, str, Any]:
    """Validate JSON string and return validation result"""
    try:
        parsed = json.loads(json_string)
        return True, "Valid JSON", parsed
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}", None

def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """Flatten nested dictionary for display"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return dict(items)

def unflatten_dict(flat_dict: Dict, sep: str = '.') -> Dict:
    """Convert flattened dictionary back to nested structure"""
    result = {}
    for key, value in flat_dict.items():
        parts = key.split(sep)
        d = result
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        
        # Handle list values
        if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
            try:
                d[parts[-1]] = json.loads(value)
            except:
                d[parts[-1]] = value
        else:
            d[parts[-1]] = value
    return result

def create_download_link(data: List[Dict], filename: str) -> str:
    """Create a download link for JSON data"""
    json_str = json.dumps(data, indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    return f'<a href="data:application/json;base64,{b64}" download="{filename}">Download {filename}</a>'

# Main UI
st.title("🧪 JSON Test Case Editor Dashboard")
st.markdown("---")

# Sidebar for actions
with st.sidebar:
    st.header("📁 Data Input")
    
    # File upload
    uploaded_file = st.file_uploader("Upload JSON file", type=['json'])
    
    # Text input
    st.subheader("Or paste JSON:")
    json_input = st.text_area("JSON Text", height=150, placeholder="Paste your JSON array here...")
    
    if st.button("Load JSON", type="primary"):
        json_data = None
        
        if uploaded_file:
            try:
                json_data = json.load(uploaded_file)
                st.success("✅ File uploaded successfully!")
            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
        
        elif json_input.strip():
            is_valid, message, json_data = validate_json(json_input.strip())
            if is_valid:
                st.success("✅ JSON loaded successfully!")
            else:
                st.error(f"❌ {message}")
        
        if json_data:
            if isinstance(json_data, list):
                st.session_state.test_cases = json_data
            else:
                st.session_state.test_cases = [json_data]
    
    st.markdown("---")
    
    # Add new test cases
    st.header("➕ Add Test Cases")
    num_cases = st.number_input("Number of cases to add", min_value=1, max_value=10, value=1)
    
    if st.button("Add Default Cases"):
        for _ in range(num_cases):
            st.session_state.test_cases.append(DEFAULT_TEST_CASE.copy())
        st.success(f"✅ Added {num_cases} default test case(s)")
    
    if st.button("Add Empty Cases"):
        for _ in range(num_cases):
            st.session_state.test_cases.append({})
        st.success(f"✅ Added {num_cases} empty test case(s)")

# Main content area
if st.session_state.test_cases:
    st.header(f"📊 Test Cases ({len(st.session_state.test_cases)} total)")
    
    # Export buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📋 Copy to Clipboard", help="Copy JSON to clipboard"):
            json_str = json.dumps(st.session_state.test_cases, indent=2)
            st.code(json_str, language='json')
            st.info("💡 Select and copy the JSON above")
    
    with col2:
        json_str = json.dumps(st.session_state.test_cases, indent=2)
        st.download_button(
            label="💾 Download JSON",
            data=json_str,
            file_name="test_cases.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # Display and edit test cases
    for i, test_case in enumerate(st.session_state.test_cases):
        with st.expander(f"🧪 Test Case {i+1}", expanded=(i == 0)):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col2:
                if st.button(f"📄 Duplicate", key=f"dup_{i}"):
                    st.session_state.test_cases.insert(i+1, test_case.copy())
                    st.rerun()
            
            with col3:
                if st.button(f"🗑️ Delete", key=f"del_{i}", type="secondary"):
                    st.session_state.test_cases.pop(i)
                    st.rerun()
            
            # JSON Editor
            st.subheader("JSON Editor")
            json_str = json.dumps(test_case, indent=2)
            edited_json = st.text_area(
                "Edit JSON",
                value=json_str,
                height=200,
                key=f"json_editor_{i}"
            )
            
            # Validate and update
            is_valid, message, parsed_json = validate_json(edited_json)
            
            if is_valid:
                st.success("✅ Valid JSON")
                if st.button(f"💾 Save Changes", key=f"save_{i}"):
                    st.session_state.test_cases[i] = parsed_json
                    st.success("✅ Changes saved!")
                    st.rerun()
            else:
                st.error(f"❌ {message}")
            
            # Tabular view for easier editing
            st.subheader("Field Editor")
            
            if test_case:
                # Flatten the JSON for easier editing
                flat_data = flatten_dict(test_case)
                
                # Group by main categories
                categories = {}
                for key, value in flat_data.items():
                    category = key.split('.')[0] if '.' in key else 'root'
                    if category not in categories:
                        categories[category] = {}
                    categories[category][key] = value
                
                # Create tabs for each category
                if categories:
                    tabs = st.tabs(list(categories.keys()))
                    updated_data = {}
                    
                    for tab, (cat_name, cat_data) in zip(tabs, categories.items()):
                        with tab:
                            cols = st.columns(2)
                            for idx, (field_key, field_value) in enumerate(cat_data.items()):
                                col = cols[idx % 2]
                                with col:
                                    # Determine input type based on value
                                    if isinstance(field_value, bool):
                                        updated_data[field_key] = st.checkbox(
                                            field_key, value=field_value, key=f"{i}_{field_key}"
                                        )
                                    elif isinstance(field_value, (int, float)):
                                        updated_data[field_key] = st.number_input(
                                            field_key, value=field_value, key=f"{i}_{field_key}"
                                        )
                                    else:
                                        updated_data[field_key] = st.text_input(
                                            field_key, value=str(field_value), key=f"{i}_{field_key}"
                                        )
                    
                    # Update button for field editor
                    if st.button(f"🔄 Update from Fields", key=f"update_fields_{i}"):
                        # Convert flattened data back to nested structure
                        updated_case = unflatten_dict(updated_data)
                        st.session_state.test_cases[i] = updated_case
                        st.success("✅ Updated from field editor!")
                        st.rerun()
            
            st.markdown("---")

else:
    # Welcome screen
    st.info("👋 Welcome! Upload a JSON file or paste JSON data in the sidebar to get started.")
    
    st.subheader("📋 Features:")
    st.markdown("""
    - **Upload JSON files** or **paste JSON text**
    - **Edit test cases** with both JSON editor and field-by-field editor
    - **Duplicate and delete** test cases
    - **Add new test cases** (default template or empty)
    - **Export functionality** (copy to clipboard or download)
    - **JSON validation** with error messages
    - **Organized editing** with categorized tabs
    """)
    
    st.subheader("🚀 Quick Start:")
    st.markdown("""
    1. Use the sidebar to upload a JSON file or paste JSON data
    2. Click "Load JSON" to import your test cases
    3. Expand any test case to start editing
    4. Use the field editor for quick changes or JSON editor for advanced editing
    5. Export your final test cases using the copy or download buttons
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Ready for GitHub deployment")
