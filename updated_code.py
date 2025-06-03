import streamlit as st
import json
import copy
from typing import Dict, List, Any, Union

# Page configuration
st.set_page_config(
    page_title="JSON Test Case Editor - Fixed",
    page_icon="🧪",
    layout="wide"
)

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

def validate_json_string(json_str: str) -> tuple[bool, str, Any]:
    """Validate and parse JSON string"""
    try:
        if not json_str.strip():
            return False, "Empty JSON", None
        parsed = json.loads(json_str)
        return True, "Valid", parsed
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}", None

# Initialize session state
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []
if 'edited_cases' not in st.session_state:
    st.session_state.edited_cases = {}

# Title
st.title("🧪 JSON Test Case Editor - Fixed Version")
st.markdown("**Fixed Issues:** ✅ Edited JSON reflected in output ✅ Blank duplicates & clean export")
st.markdown("---")

# Sidebar for file upload
with st.sidebar:
    st.header("📁 Upload JSON")
    uploaded_file = st.file_uploader("Choose JSON file", type=['json'])
    
    if uploaded_file:
        try:
            json_data = json.load(uploaded_file)
            if isinstance(json_data, list):
                st.session_state.test_cases = json_data
                # Initialize edited cases with original data
                st.session_state.edited_cases = {
                    i: json.dumps(case, indent=2) for i, case in enumerate(json_data)
                }
                st.success(f"✅ Loaded {len(json_data)} test cases")
            else:
                st.session_state.test_cases = [json_data]
                st.session_state.edited_cases = {0: json.dumps(json_data, indent=2)}
                st.success("✅ Loaded 1 test case")
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")

# Main content
if st.session_state.test_cases:
    st.header(f"📊 Test Cases ({len(st.session_state.test_cases)} total)")
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📄 Add Blank Row"):
            if st.session_state.test_cases:
                # Create blank structure based on first test case
                template = st.session_state.test_cases[0]
                blank_case = create_blank_structure(template)
            else:
                blank_case = {}
            
            new_index = len(st.session_state.test_cases)
            st.session_state.test_cases.append(blank_case)
            st.session_state.edited_cases[new_index] = json.dumps(blank_case, indent=2)
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear All"):
            st.session_state.test_cases = []
            st.session_state.edited_cases = {}
            st.rerun()
    
    st.markdown("---")
    
    # Display and edit test cases
    for i, original_case in enumerate(st.session_state.test_cases):
        with st.expander(f"🧪 Test Case {i+1}", expanded=(i == 0)):
            
            # Action buttons for each row
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button(f"📄 Duplicate as Blank", key=f"dup_{i}"):
                    blank_case = create_blank_structure(original_case)
                    new_index = len(st.session_state.test_cases)
                    st.session_state.test_cases.append(blank_case)
                    st.session_state.edited_cases[new_index] = json.dumps(blank_case, indent=2)
                    st.rerun()
            
            with col2:
                if st.button(f"🗑️ Delete", key=f"del_{i}"):
                    st.session_state.test_cases.pop(i)
                    # Reindex edited_cases
                    new_edited = {}
                    for idx, case in enumerate(st.session_state.test_cases):
                        if idx < i and idx in st.session_state.edited_cases:
                            new_edited[idx] = st.session_state.edited_cases[idx]
                        elif idx >= i and (idx + 1) in st.session_state.edited_cases:
                            new_edited[idx] = st.session_state.edited_cases[idx + 1]
                        else:
                            new_edited[idx] = json.dumps(case, indent=2)
                    st.session_state.edited_cases = new_edited
                    st.rerun()
            
            # JSON Editor
            if i not in st.session_state.edited_cases:
                st.session_state.edited_cases[i] = json.dumps(original_case, indent=2)
            
            edited_json = st.text_area(
                f"Edit JSON for Test Case {i+1}",
                value=st.session_state.edited_cases[i],
                height=300,
                key=f"json_editor_{i}"
            )
            
            # Update the edited_cases when text area changes
            if edited_json != st.session_state.edited_cases[i]:
                st.session_state.edited_cases[i] = edited_json
            
            # Validate current JSON
            is_valid, message, parsed_data = validate_json_string(edited_json)
            
            if is_valid:
                st.success("✅ Valid JSON")
            else:
                st.error(f"❌ {message}")
    
    st.markdown("---")
    
    # Export section
    st.header("📤 Export")
    
    # Process all edited cases
    final_cases = []
    validation_errors = []
    
    for i, edited_json in st.session_state.edited_cases.items():
        if i < len(st.session_state.test_cases):  # Make sure index is valid
            is_valid, message, parsed_data = validate_json_string(edited_json)
            
            if is_valid and parsed_data is not None:
                # Clean the data (remove empty fields)
                cleaned_case = clean_dict(parsed_data)
                
                # Only include non-blank cases
                if not is_entirely_blank(parsed_data):
                    final_cases.append(cleaned_case)
            else:
                validation_errors.append(f"Test Case {i+1}: {message}")
    
    # Show validation errors if any
    if validation_errors:
        st.error("❌ **Validation Errors:**")
        for error in validation_errors:
            st.error(f"• {error}")
    
    # Export buttons and preview
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(f"📊 Final Output ({len(final_cases)} cases)")
        if final_cases:
            final_json = json.dumps(final_cases, indent=2)
            
            # Copy to clipboard button
            if st.button("📋 Copy to Clipboard", type="primary"):
                st.success("✅ **JSON ready to copy below:**")
                st.code(final_json, language='json')
                st.info("💡 Select all text above and copy (Ctrl+A, Ctrl+C)")
        else:
            st.warning("⚠️ No valid test cases to export")
    
    with col2:
        st.subheader("📥 Download")
        if final_cases:
            final_json = json.dumps(final_cases, indent=2)
            st.download_button(
                label="💾 Download JSON File",
                data=final_json,
                file_name="cleaned_test_cases.json",
                mime="application/json"
            )
        
        # Statistics
        st.markdown("**Statistics:**")
        st.write(f"• Original cases: {len(st.session_state.test_cases)}")
        st.write(f"• Valid cases: {len(final_cases)}")
        st.write(f"• Validation errors: {len(validation_errors)}")

else:
    # Welcome screen
    st.info("👋 **Welcome!** Please upload a JSON file using the sidebar to get started.")
    
    st.subheader("✅ **Fixed Issues:**")
    st.markdown("""
    1. **Edited JSON Reflection**: Changes in text areas are now properly captured and used in the final output
    2. **Blank Duplicates**: Duplicated rows now start with blank/null values while keeping the same structure
    3. **Clean Export**: 
       - Empty fields are excluded from the final JSON
       - Entirely blank rows are excluded
       - Only valid JSON is included in the export
    """)
    
    st.subheader("🚀 **How to Use:**")
    st.markdown("""
    1. **Upload** your JSON file using the sidebar
    2. **Edit** test cases using the text areas (changes are automatically tracked)
    3. **Duplicate** rows as blank templates or **add** new blank rows
    4. **Export** cleaned JSON with the "Copy to Clipboard" button
    """)

# Footer
st.markdown("---")
st.markdown("🔧 **Fixed Version** - Issues resolved: JSON reflection & clean export")
