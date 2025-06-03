import streamlit as st
import json
import copy
from typing import Dict, Any, List

# Page configuration
st.set_page_config(
    page_title="Health Score API JSON Tester",
    page_icon="🏥",
    layout="wide"
)

def get_default_json_structure() -> Dict[str, Any]:
    """Returns the default JSON structure with all values set to null/empty"""
    return {
        "mhm": {
            "age": None,
            "hgt": None,
            "wgt": None,
            "sex": None,
            "dbp": None,
            "map": None,
            "sbp": None,
            "fat": None,
            "ppr": None,
            "rhr": None,
            "rhr_day": [],
            "spo2": None,
            "vo2max": None,
            "whr": None,
            "wst": None,
            "alc": None,
            "cst": None,
            "exh": None,
            "fCV": None,
            "fDM": None,
            "fMI": None,
            "pHT": None,
            "a1c": None,
            "acr": None,
            "cre": None,
            "crp": None,
            "cys": None,
            "fbg": None,
            "eag": None,
            "gfr": None,
            "hdl": None,
            "ldl": None,
            "tgl": None,
            "tsc": None,
            "vdl": None,
            "CAN": None,
            "CHD": None,
            "CHF": None,
            "CKD": None,
            "CVD": None,
            "DM2": None,
            "HTN": None,
            "LDS": None,
            "LVH": None,
            "PDM": None,
            "PMI": None,
            "STK": None,
            "TDM": None,
            "THT": None
        },
        "smk": {
            "now": None,
            "evr": None,
            "yrs": None,
            "num": None,
            "qit": None,
            "slt": None,
        },
        "slp": {
            "bed": [],
            "slp": [],
            "awk": [],
            "slp_avg": []
        },
        "nut": {
            "nqs01": None,
            "nqs02": None,
            "nqs03": None,
            "nqs04": None,
            "nqs05": None,
            "nqs06": None,
            "nqs07": None,
            "nqs08": None,
            "nqs09": None,
            "nqs10": None,
            "nqs11": None,
            "nqs12": None,
            "nqs13": None,
            "nqs14": None,
            "nqs15": None,
            "nqs16": None,
            "nqs17": None,
            "nqs18": None,
            "nqs19": None,
            "nqs20": None,
            "nqs21": None,
            "nqs22": None,
            "protein": None,
            "sfat": None,
            "sugar": None,
            "fiber": None,
            "sodium": None,
            "vitamin_c": None,
            "iron": None,
            "percentage_drink": None,
            "density_drink": None,
        },
        "qlm": {
            "q01": None,
            "q02": None,
            "q03": None,
            "q04": None,
            "q05": None,
            "q06": None,
            "q07": None,
            "q08": None,
            "q09": None,
            "q10": None,
            "q11": None,
            "q12": None,
            "q13": None,
            "q14": None,
            "q15": None,
            "q16": None,
            "q17": None,
            "q18": None,
            "q19": None,
            "q20": None,
            "q21": None,
            "q22": None,
            "q23": None,
            "q24": None,
            "q25": None,
            "q26": None,
            "q27": None,
            "gad01": None,
            "gad02": None,
            "gad03": None,
            "gad04": None,
            "gad05": None,
            "gad06": None,
            "gad07": None,
            "phq01": None,
            "phq02": None,
            "phq03": None,
            "phq04": None,
            "phq05": None,
            "phq06": None,
            "phq07": None,
            "phq08": None,
            "phq09": None,
            "pss01": None,
            "pss02": None,
            "pss03": None,
            "pss04": None,
            "pss05": None,
            "pss06": None,
            "pss07": None,
            "pss08": None,
            "pss09": None,
            "pss10": None,
            "gsrh": None,
            "maas01": None,
            "maas02": None,
            "maas03": None,
            "maas04": None,
            "maas05": None,
            "maas06": None,
            "maas07": None,
            "maas08": None,
            "maas09": None,
            "maas10": None,
            "maas11": None,
            "maas12": None,
            "maas13": None,
            "maas14": None,
            "maas15": None,
            "mfm": [],
        },
        "clip": None
    }

def remove_null_values(data: Any) -> Any:
    """Recursively remove null/None values from nested dictionaries and lists"""
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            cleaned_value = remove_null_values(value)
            # Only include non-null, non-empty values
            if (cleaned_value is not None and 
                cleaned_value != [] and 
                cleaned_value != {} and 
                cleaned_value != "" and
                str(cleaned_value).lower() != "null"):
                cleaned[key] = cleaned_value
        return cleaned if cleaned else None
    elif isinstance(data, list):
        cleaned = []
        for item in data:
            cleaned_item = remove_null_values(item)
            # Only include non-null, non-empty items
            if (cleaned_item is not None and 
                cleaned_item != "" and 
                str(cleaned_item).lower() != "null"):
                cleaned.append(cleaned_item)
        return cleaned if cleaned else None
    else:
        # Return None for null, None, empty string, or "null" string values
        if (data is None or 
            data == "" or 
            str(data).lower() == "null"):
            return None
        return data

def is_form_empty(form_data: Dict[str, Any]) -> bool:
    """Check if a form is completely empty (all values are null/None/empty)"""
    cleaned = remove_null_values(form_data)
    return cleaned is None or cleaned == {}

def copy_to_clipboard_js(text: str) -> str:
    """Generate JavaScript code to copy text to clipboard"""
    # Escape special characters for JavaScript
    escaped_text = text.replace('\\', '\\\\').replace('`', '\\`').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
    return f"""
    <div id="copy-section">
        <script>
        (function() {{
            const textToCopy = `{escaped_text}`;
            
            async function copyToClipboard() {{
                try {{
                    if (navigator.clipboard && window.isSecureContext) {{
                        await navigator.clipboard.writeText(textToCopy);
                        alert('✅ JSON copied to clipboard successfully!');
                    }} else {{
                        // Fallback for older browsers or non-HTTPS
                        const textArea = document.createElement('textarea');
                        textArea.value = textToCopy;
                        textArea.style.position = 'fixed';
                        textArea.style.left = '-999999px';
                        textArea.style.top = '-999999px';
                        document.body.appendChild(textArea);
                        textArea.focus();
                        textArea.select();
                        
                        try {{
                            document.execCommand('copy');
                            alert('✅ JSON copied to clipboard successfully!');
                        }} catch (err) {{
                            console.error('Fallback copy failed: ', err);
                            alert('❌ Copy failed. Please copy manually from the text area below.');
                        }}
                        
                        document.body.removeChild(textArea);
                    }}
                }} catch (err) {{
                    console.error('Copy failed: ', err);
                    alert('❌ Copy failed. Please copy manually from the text area below.');
                }}
            }}
            
            // Execute copy immediately
            copyToClipboard();
        }})();
        </script>
    </div>
    """

# Initialize session state
if 'forms' not in st.session_state:
    st.session_state.forms = [get_default_json_structure()]
if 'form_counter' not in st.session_state:
    st.session_state.form_counter = 1

# Main UI
st.title("🏥 Health Score API JSON Testing Dashboard")
st.markdown("---")

# Control buttons
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    if st.button("➕ Add New Test Case", type="primary"):
        st.session_state.forms.append(get_default_json_structure())
        st.session_state.form_counter += 1
        st.rerun()

with col2:
    if st.button("🗑️ Clear All Forms", type="secondary"):
        st.session_state.forms = [get_default_json_structure()]
        st.session_state.form_counter = 1
        st.rerun()

with col3:
    # Copy to clipboard button
    if st.button("📋 Copy All to Clipboard", type="primary"):
        # Collect all non-empty forms
        valid_forms = []
        for i, form_data in enumerate(st.session_state.forms):
            if not is_form_empty(form_data):
                cleaned_form = remove_null_values(form_data)
                if cleaned_form:
                    valid_forms.append(cleaned_form)
        
        if valid_forms:
            json_output = json.dumps(valid_forms, indent=2)
            # Display the JSON that will be copied
            st.success("✅ Ready to copy!")
            st.text_area("JSON to be copied:", value=json_output, height=200, key="copy_preview")
            # Use JavaScript to copy to clipboard
            st.components.v1.html(copy_to_clipboard_js(json_output), height=50)
        else:
            st.warning("No valid forms to copy!")

st.markdown("---")

# Display forms
for i, form_data in enumerate(st.session_state.forms):
    with st.expander(f"🧪 Test Case {i + 1}", expanded=True):
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown("**Actions:**")
            if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                if len(st.session_state.forms) > 1:
                    st.session_state.forms.pop(i)
                    st.rerun()
                else:
                    st.warning("Cannot delete the last form!")
            
            if st.button(f"📋 Copy This Form", key=f"copy_{i}"):
                if not is_form_empty(form_data):
                    cleaned_form = remove_null_values(form_data)
                    if cleaned_form:
                        json_output = json.dumps([cleaned_form], indent=2)
                        st.success("✅ Ready to copy!")
                        st.text_area("JSON to be copied:", value=json_output, height=150, key=f"copy_preview_{i}")
                        st.components.v1.html(copy_to_clipboard_js(json_output), height=50)
                else:
                    st.warning("Form is empty!")
        
        with col2:
            # JSON editor for this form
            json_str = json.dumps(form_data, indent=2)
            edited_json = st.text_area(
                f"Edit JSON for Test Case {i + 1}:",
                value=json_str,
                height=400,
                key=f"json_editor_{i}"
            )
            
            # Try to parse and update the form data
            try:
                parsed_json = json.loads(edited_json)
                st.session_state.forms[i] = parsed_json
                st.success("✅ Valid JSON")
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON: {str(e)}")

# Footer information
st.markdown("---")
st.markdown("### 📋 Usage Instructions:")
st.markdown("""
1. **Edit JSON**: Modify the JSON structure in each text area
2. **Add Test Cases**: Click "Add New Test Case" to create more forms
3. **Copy to Clipboard**: Use the copy buttons to get cleaned JSON (null values removed)
4. **Valid Forms Only**: Empty forms are automatically excluded from clipboard copy
5. **Real-time Validation**: JSON syntax errors are highlighted immediately
""")

st.markdown("### 🔧 Features:")
st.markdown("""
- ✅ Multiple test cases with individual editing
- ✅ Automatic null/empty value removal
- ✅ Real-time JSON validation
- ✅ Clipboard integration
- ✅ Form duplication and deletion
- ✅ Clean, organized interface
""")

# Display current form count
st.sidebar.markdown(f"**Current Test Cases:** {len(st.session_state.forms)}")
st.sidebar.markdown("**Default Structure Fields:**")
st.sidebar.json({
    "mhm": "Medical/Health Measurements",
    "smk": "Smoking Data", 
    "slp": "Sleep Data",
    "nut": "Nutrition Data",
    "qlm": "Quality of Life Measurements",
    "clip": "Clipboard flag"
})
