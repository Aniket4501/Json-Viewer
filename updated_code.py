import streamlit as st
import json
import copy
from typing import Dict, List, Any, Union
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="JSON Test Case Editor - Enhanced",
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

def create_blank_structure(template: Dict) -> Dict:
    """Create a blank structure with same keys but empty/null values"""
    def make_blank(obj):
        if isinstance(obj, dict):
            return {k: make_blank(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return []
        elif isinstance(obj, str):
            return ""
        elif isinstance(obj, (int, float)):
            return None
        elif isinstance(obj, bool):
            return None
        else:
            return None
    
    return make_blank(template)

def is_empty_value(value: Any) -> bool:
    """Check if a value is considered empty"""
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    if isinstance(value, dict) and len(value) == 0:
        return True
    return False

def clean_dict(obj: Dict) -> Dict:
    """Remove empty fields from a dictionary recursively"""
    if isinstance(obj, dict):
        cleaned = {}
        for key, value in obj.items():
            if isinstance(value, dict):
                cleaned_nested = clean_dict(value)
                if cleaned_nested:  # Only add if not empty after cleaning
                    cleaned[key] = cleaned_nested
            elif not is_empty_value(value):
                cleaned[key] = value
        return cleaned
    return obj

def is_entirely_blank(obj: Dict) -> bool:
    """Check if an object is entirely blank after cleaning"""
    cleaned = clean_dict(obj)
    return len(cleaned) == 0

def validate_json(json_string: str) -> tuple[bool, str, Any]:
    """Validate JSON string and return validation result"""
    try:
        if not json_string.strip():
            return False, "Empty JSON", None
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

# Initialize session state
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []
if 'edited_cases' not in st.session_state:
    st.session_state.edited_cases = {}
if 'field_updates' not in st.session_state:
    st.session_state.field_updates = {}

# Main UI
st.title("🧪 JSON Test Case Editor - Enhanced Version")
st.markdown("**Features:** ✅ Multi-editor support ✅ Auto clipboard copy ✅ Clean export ✅ Blank duplicates")
st.markdown("---")

# Sidebar for data input
with st.sidebar:
    st.header("📁 Load JSON Data")
    
    # Option 1: File upload
    st.subheader("Upload File")
    uploaded_file = st.file_uploader("Choose JSON file", type=['json'])
    
    # Option 2: Paste JSON
    st.subheader("Or Paste JSON")
    json_input = st.text_area(
        "Paste JSON array here", 
        height=150, 
        placeholder='[\n  {\n    "key": "value"\n  }\n]'
    )
    
    # Load button
    if st.button("🚀 Load JSON", type="primary"):
        json_data = None
        
        # Try file first, then pasted text
        if uploaded_file:
            try:
                json_data = json.load(uploaded_file)
                source = "file"
            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
        
        elif json_input.strip():
            is_valid, message, parsed_data = validate_json(json_input.strip())
            if is_valid:
                json_data = parsed_data
                source = "pasted text"
            else:
                st.error(f"❌ {message}")
        
        else:
            st.warning("⚠️ Please upload a file or paste JSON data")
        
        # Process the loaded data
        if json_data:
            if isinstance(json_data, list):
                st.session_state.test_cases = json_data
                # Initialize edited cases with original data
                st.session_state.edited_cases = {
                    i: json.dumps(case, indent=2) for i, case in enumerate(json_data)
                }
                st.session_state.field_updates = {}
                st.success(f"✅ Loaded {len(json_data)} test cases from {source}")
            else:
                st.session_state.test_cases = [json_data]
                st.session_state.edited_cases = {0: json.dumps(json_data, indent=2)}
                st.session_state.field_updates = {}
                st.success(f"✅ Loaded 1 test case from {source}")
            
            # Clear the input after successful load
            if source == "pasted text":
                st.rerun()
    
    st.markdown("---")
    
    # Add new test cases
    st.header("➕ Add Test Cases")
    num_cases = st.number_input("Number of cases to add", min_value=1, max_value=10, value=1)
    
    if st.button("Add Default Cases"):
        for _ in range(num_cases):
            new_index = len(st.session_state.test_cases)
            st.session_state.test_cases.append(DEFAULT_TEST_CASE.copy())
            st.session_state.edited_cases[new_index] = json.dumps(DEFAULT_TEST_CASE, indent=2)
        st.success(f"✅ Added {num_cases} default test case(s)")
        st.rerun()
    
    if st.button("Add Blank Cases"):
        template = DEFAULT_TEST_CASE if not st.session_state.test_cases else st.session_state.test_cases[0]
        for _ in range(num_cases):
            blank_case = create_blank_structure(template)
            new_index = len(st.session_state.test_cases)
            st.session_state.test_cases.append(blank_case)
            st.session_state.edited_cases[new_index] = json.dumps(blank_case, indent=2)
        st.success(f"✅ Added {num_cases} blank test case(s)")
        st.rerun()

# Main content area
if st.session_state.test_cases:
    st.header(f"📊 Test Cases ({len(st.session_state.test_cases)} total)")
    
    # Export buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    # Process all edited cases for export
    final_cases = []
    validation_errors = []
    
    for i in range(len(st.session_state.test_cases)):
        # Get the latest data from either JSON editor or field updates
        if i in st.session_state.field_updates:
            # Use field updates if available
            test_case_data = st.session_state.field_updates[i]
        elif i in st.session_state.edited_cases:
            # Parse from JSON editor
            is_valid, message, parsed_data = validate_json(st.session_state.edited_cases[i])
            if is_valid and parsed_data is not None:
                test_case_data = parsed_data
            else:
                validation_errors.append(f"Test Case {i+1}: {message}")
                continue
        else:
            # Use original data
            test_case_data = st.session_state.test_cases[i]
        
        # Clean the data (remove empty fields)
        cleaned_case = clean_dict(test_case_data)
        
        # Only include non-blank cases
        if not is_entirely_blank(test_case_data):
            final_cases.append(cleaned_case)
    
    with col1:
        if st.button("📋 Copy to Clipboard", help="Automatically copy JSON to clipboard"):
            if final_cases:
                final_json = json.dumps(final_cases, indent=2)
                # Use Streamlit's built-in clipboard functionality
                st.write("🎯 **JSON copied to clipboard!**")
                st.code(final_json, language='json')
                # JavaScript to copy to clipboard
                st.components.v1.html(f"""
                <script>
                navigator.clipboard.writeText(`{final_json.replace('`', '\\`')}`).then(function() {{
                    console.log('JSON copied to clipboard successfully!');
                }}, function(err) {{
                    console.error('Could not copy text: ', err);
                }});
                </script>
                """, height=0)
                st.success("✅ JSON automatically copied to clipboard!")
            else:
                st.warning("⚠️ No valid test cases to copy")
    
    with col2:
        if final_cases:
            final_json = json.dumps(final_cases, indent=2)
            st.download_button(
                label="💾 Download JSON",
                data=final_json,
                file_name="test_cases.json",
                mime="application/json"
            )
    
    with col3:
        if validation_errors:
            st.error(f"⚠️ {len(validation_errors)} validation errors")
        st.write(f"📊 **Export:** {len(final_cases)} valid cases")
    
    st.markdown("---")
    
    # Display and edit test cases
    for i, test_case in enumerate(st.session_state.test_cases):
        with st.expander(f"🧪 Test Case {i+1}", expanded=(i == 0)):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col2:
                if st.button(f"📄 Duplicate as Blank", key=f"dup_{i}"):
                    blank_case = create_blank_structure(test_case)
                    new_index = len(st.session_state.test_cases)
                    st.session_state.test_cases.append(blank_case)
                    st.session_state.edited_cases[new_index] = json.dumps(blank_case, indent=2)
                    st.rerun()
            
            with col3:
                if st.button(f"🗑️ Delete", key=f"del_{i}", type="secondary"):
                    st.session_state.test_cases.pop(i)
                    # Clean up session state
                    if i in st.session_state.edited_cases:
                        del st.session_state.edited_cases[i]
                    if i in st.session_state.field_updates:
                        del st.session_state.field_updates[i]
                    st.rerun()
            
            # Create tabs for different editors
            tab1, tab2 = st.tabs(["📝 JSON Editor", "🎛️ Field Editor"])
            
            with tab1:
                # JSON Editor
                if i not in st.session_state.edited_cases:
                    st.session_state.edited_cases[i] = json.dumps(test_case, indent=2)
                
                edited_json = st.text_area(
                    "Edit JSON",
                    value=st.session_state.edited_cases[i],
                    height=300,
                    key=f"json_editor_{i}"
                )
                
                # Update the edited_cases when text area changes
                if edited_json != st.session_state.edited_cases[i]:
                    st.session_state.edited_cases[i] = edited_json
                
                # Validate and save
                is_valid, message, parsed_json = validate_json(edited_json)
                
                if is_valid:
                    st.success("✅ Valid JSON")
                    if st.button(f"💾 Save JSON Changes", key=f"save_json_{i}"):
                        st.session_state.test_cases[i] = parsed_json
                        # Clear field updates for this case
                        if i in st.session_state.field_updates:
                            del st.session_state.field_updates[i]
                        st.success("✅ JSON changes saved!")
                        st.rerun()
                else:
                    st.error(f"❌ {message}")
            
            with tab2:
                # Field Editor
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
                        cat_tabs = st.tabs(list(categories.keys()))
                        updated_data = {}
                        
                        for tab, (cat_name, cat_data) in zip(cat_tabs, categories.items()):
                            with tab:
                                cols = st.columns(2)
                                for idx, (field_key, field_value) in enumerate(cat_data.items()):
                                    col = cols[idx % 2]
                                    with col:
                                        # Determine input type based on value
                                        if isinstance(field_value, bool):
                                            updated_data[field_key] = st.checkbox(
                                                field_key, value=field_value, key=f"field_{i}_{field_key}"
                                            )
                                        elif isinstance(field_value, (int, float)):
                                            updated_data[field_key] = st.number_input(
                                                field_key, value=field_value, key=f"field_{i}_{field_key}"
                                            )
                                        else:
                                            updated_data[field_key] = st.text_input(
                                                field_key, value=str(field_value), key=f"field_{i}_{field_key}"
                                            )
                        
                        # Update button for field editor
                        if st.button(f"🔄 Save Field Changes", key=f"update_fields_{i}"):
                            # Convert flattened data back to nested structure
                            updated_case = unflatten_dict(updated_data)
                            st.session_state.field_updates[i] = updated_case
                            st.session_state.test_cases[i] = updated_case
                            # Update JSON editor too
                            st.session_state.edited_cases[i] = json.dumps(updated_case, indent=2)
                            st.success("✅ Field changes saved!")
                            st.rerun()
            
            st.markdown("---")

else:
    # Welcome screen
    st.info("👋 **Welcome!** Please upload a JSON file or paste JSON data using the sidebar to get started.")
    
    st.subheader("✨ **Enhanced Features:**")
    st.markdown("""
    - **📝 Dual Editors**: JSON text editor + interactive field editor with categories
    - **📋 Auto Clipboard**: One-click copying with automatic clipboard functionality
    - **🎯 Smart Export**: Removes empty fields and blank rows automatically
    - **📄 Blank Duplicates**: Creates empty templates maintaining structure
    - **🔄 Real-time Sync**: Changes sync between JSON and field editors
    - **✅ Validation**: Live JSON validation with detailed error messages
    """)
    
    st.subheader("🚀 **How to Use:**")
    st.markdown("""
    1. **Load Data**: Upload JSON file OR paste JSON data, then click "Load JSON"
    2. **Edit**: Use either the JSON editor (raw text) or Field editor (form-based)
    3. **Duplicate**: Create blank copies using "Duplicate as Blank"
    4. **Export**: Click "Copy to Clipboard" for automatic copying or download JSON
    """)

# Footer
st.markdown("---")
st.markdown("🚀 **Enhanced Version** - Combined best features with automatic clipboard copying")
