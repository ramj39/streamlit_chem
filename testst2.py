import streamlit as st
import requests

st.set_page_config(page_title="Get CID & SMILES from Vompound Name", layout="wide")
st.title("🔬 CID & SMILES ")
st.write("Enter a compound name or CID number to retrieve its Isomeric SMILES from PubChem.")

# Input field for compound name
name = st.text_input("Compound Name:")

# Input field for CID number
cid = st.text_input("CID Number:")

# Fetch CID from compound name
if name:
    try:
        url_name = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/JSON"
        response_name = requests.get(url_name)
        if response_name.status_code == 200:
            name_data = response_name.json()
            if "IdentifierList" in name_data and "CID" in name_data["IdentifierList"]:
                cid_list = name_data["IdentifierList"]["CID"]
                st.write("🔍 Retrieved CID from name:")
                st.json(cid_list)
            else:
                st.warning("No CID found for the given compound name.")
        else:
            st.warning("Compound name not found.")
    except Exception as e:
        st.error(f"Error fetching CID from name: {e}")

# Fetch Isomeric SMILES from CID
if cid:
    if cid.isdigit():  # Check if CID is numeric
        try:
            url_cid = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/IsomericSMILES/JSON"
            response_cid = requests.get(url_cid)
            if response_cid.status_code == 200:
                data = response_cid.json()
                st.write("🧪 API Response:")
                st.json(data)

                if "PropertyTable" in data and "Properties" in data["PropertyTable"]:
                    properties = data["PropertyTable"]["Properties"]
                    if properties:
                        isomeric_smiles = properties[0].get("IsomericSMILES")
                        if isomeric_smiles:
                            st.success(f"**Isomeric SMILES for CID {cid}:**")
                            st.write(isomeric_smiles)
                        else:
                            st.warning("Isomeric SMILES not found.")
                    else:
                        st.warning("No properties found for this CID.")
                else:
                    st.warning("Unexpected response structure.")
            else:
                st.warning(f"CID not found in PubChem. Status code: {response_cid.status_code}")
        except Exception as e:
            st.error(f"Error fetching SMILES from CID: {e}")
    else:
        st.warning("Please enter a valid numeric CID.")
