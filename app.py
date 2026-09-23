import streamlit as st

from crypto_utils import (
    load_or_create_key,
    encrypt_data,
    decrypt_data,
    calculate_sha256
)

from blockchain import Blockchain
from auth import authenticate_user

from storage import (
    patient_id_exists,
    save_record,
    get_all_records
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EHR Blockchain Security",
    page_icon="🔐",
    layout="wide"
)


# ============================================================
# LOAD BLOCKCHAIN FROM STORAGE
# ============================================================

def load_blockchain():

    blockchain = Blockchain()

    stored_records = get_all_records()

    for record in stored_records:

        blockchain.add_existing_block(
            encrypted_data=record["encrypted_data"],
            data_hash=record["data_hash"],
            block_hash=record["block_hash"],
            previous_hash=record["previous_hash"],
            timestamp=record["timestamp"]
        )

    return blockchain


# ============================================================
# SESSION STATE
# ============================================================

if "blockchain" not in st.session_state:

    st.session_state.blockchain = load_blockchain()


if "aes_key" not in st.session_state:

    st.session_state.aes_key = load_or_create_key()


if "authenticated" not in st.session_state:

    st.session_state.authenticated = False


if "username" not in st.session_state:

    st.session_state.username = None


if "role" not in st.session_state:

    st.session_state.role = None


# ============================================================
# LOGIN
# ============================================================

if not st.session_state.authenticated:

    st.title(
        "🔐 EHR Blockchain Security System"
    )

    st.subheader(
        "🔑 Authorized Login"
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        role = authenticate_user(
            username,
            password
        )

        if role:

            st.session_state.authenticated = True

            st.session_state.username = username

            st.session_state.role = role

            st.success(
                f"Login successful! Welcome {role}."
            )

            st.rerun()

        else:

            st.error(
                "❌ Invalid username or password."
            )

    st.info(
        "Only authorized users can access patient records."
    )

    st.stop()


# ============================================================
# AUTOMATIC BLOCKCHAIN INTEGRITY CHECK
# ============================================================

blockchain_is_valid = (
    st.session_state.blockchain.verify_chain()
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🔐 EHR Blockchain Security System"
)

st.write(
    "A cryptographic security model for protecting "
    "Electronic Health Records using AES-256, "
    "SHA-256 and Blockchain."
)

st.write(
    f"👤 Logged in as: **{st.session_state.username}** "
    f"({st.session_state.role})"
)


# ============================================================
# AUTOMATIC SECURITY STATUS
# ============================================================

if blockchain_is_valid:

    st.success(
        "✅ Blockchain integrity verified. "
        "No tampering detected."
    )

else:

    st.error(
        "🚨 TAMPER DETECTED! "
        "Blockchain integrity has been compromised."
    )


# ============================================================
# SECURITY ARCHITECTURE
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🔐 Encryption",
        "AES-256"
    )


with col2:

    st.metric(
        "🔑 Hashing",
        "SHA-256"
    )


with col3:

    st.metric(
        "⛓️ Storage",
        "Blockchain"
    )


with col4:

    if blockchain_is_valid:

        st.metric(
            "🛡️ Security",
            "Verified"
        )

    else:

        st.metric(
            "🛡️ Security",
            "Tampered"
        )


st.divider()


# ============================================================
# LOGOUT
# ============================================================

if st.button(
    "🚪 Logout"
):

    st.session_state.authenticated = False

    st.session_state.username = None

    st.session_state.role = None

    st.rerun()


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "🏥 Patient Record",
        "⛓️ Blockchain",
        "🔓 Authorized Access"
    ]
)


# ============================================================
# TAB 1 — PATIENT RECORD
# ============================================================

with tab1:

    st.header(
        "🏥 Secure Patient Record"
    )

    st.write(
        "Enter patient information and securely store it "
        "using AES-256 encryption and blockchain."
    )


    patient_name = st.text_input(
        "Patient Name"
    )


    patient_id = st.text_input(
        "Patient ID"
    )


    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=21
    )


    blood_group = st.selectbox(
        "Blood Group",
        [
            "A+",
            "A-",
            "B+",
            "B-",
            "AB+",
            "AB-",
            "O+",
            "O-"
        ]
    )


    diagnosis = st.text_input(
        "Diagnosis"
    )


    st.divider()


    if st.button(
        "🔐 Secure Patient Record",
        use_container_width=True
    ):

        # ----------------------------------------------------
        # CHECK REQUIRED FIELDS
        # ----------------------------------------------------

        if not patient_name or not patient_id or not diagnosis:

            st.warning(
                "⚠️ Please fill in all required fields."
            )


        else:

            # ------------------------------------------------
            # CHECK DUPLICATE PATIENT ID
            # ------------------------------------------------

            if patient_id_exists(patient_id):

                st.error(
                    "❌ Patient ID already exists. "
                    "Please use a unique Patient ID."
                )


            else:

                # --------------------------------------------
                # CREATE PATIENT RECORD
                # --------------------------------------------

                patient_record = (
                    f"Name: {patient_name}\n"
                    f"Patient ID: {patient_id}\n"
                    f"Age: {age}\n"
                    f"Blood Group: {blood_group}\n"
                    f"Diagnosis: {diagnosis}"
                )


                # --------------------------------------------
                # AES-256 ENCRYPTION
                # --------------------------------------------

                encrypted_data = encrypt_data(
                    patient_record,
                    st.session_state.aes_key
                )


                # --------------------------------------------
                # SHA-256 HASH
                # --------------------------------------------

                data_hash = calculate_sha256(
                    encrypted_data
                )


                # --------------------------------------------
                # ADD BLOCK TO BLOCKCHAIN
                # --------------------------------------------

                new_block = (
                    st.session_state.blockchain.add_block(
                        encrypted_data,
                        data_hash
                    )
                )


                # --------------------------------------------
                # SAVE TO CSV
                # --------------------------------------------

                save_record(
                    patient_id=patient_id,
                    encrypted_data=encrypted_data,
                    data_hash=data_hash,
                    block_hash=new_block.hash,
                    previous_hash=new_block.previous_hash,
                    timestamp=new_block.timestamp
                )


                # --------------------------------------------
                # SUCCESS MESSAGE
                # --------------------------------------------

                st.success(
                    "✅ Patient record secured and stored successfully!"
                )


                st.info(
                    "The patient data was encrypted using "
                    "AES-256, hashed using SHA-256 and added "
                    "to the blockchain."
                )


                # --------------------------------------------
                # SHOW ENCRYPTED DATA
                # --------------------------------------------

                st.subheader(
                    "🔐 AES-256 Encrypted Data"
                )

                st.code(
                    encrypted_data
                )


                # --------------------------------------------
                # SHOW HASH
                # --------------------------------------------

                st.subheader(
                    "🔑 SHA-256 Hash"
                )

                st.code(
                    data_hash
                )


                # --------------------------------------------
                # SHOW BLOCK HASH
                # --------------------------------------------

                st.subheader(
                    "⛓️ Blockchain Block Hash"
                )

                st.code(
                    new_block.hash
                )


# ============================================================
# TAB 2 — BLOCKCHAIN
# ============================================================

with tab2:

    st.header(
        "⛓️ Blockchain"
    )


    total_blocks = len(
        st.session_state.blockchain.chain
    )


    patient_records = total_blocks - 1


    stat1, stat2 = st.columns(2)


    with stat1:

        st.metric(
            "⛓️ Total Blocks",
            total_blocks
        )


    with stat2:

        st.metric(
            "🏥 Patient Records",
            patient_records
        )


    st.divider()


    for block in st.session_state.blockchain.chain:

        with st.expander(
            f"Block {block.index}"
        ):

            st.write(
                "**Timestamp:**",
                block.timestamp
            )


            st.write(
                "**Data Hash:**"
            )

            st.code(
                block.data_hash
            )


            st.write(
                "**Previous Block Hash:**"
            )

            st.code(
                block.previous_hash
            )


            st.write(
                "**Current Block Hash:**"
            )

            st.code(
                block.hash
            )


            if block.index != 0:

                st.write(
                    "**Encrypted Patient Data:**"
                )

                st.code(
                    block.encrypted_data
                )


# ============================================================
# TAB 3 — AUTHORIZED ACCESS
# ============================================================

with tab3:

    st.header(
        "🔓 Authorized Patient Record Access"
    )

    st.write(
        "Only authenticated users can access and "
        "decrypt patient records."
    )


    if len(
        st.session_state.blockchain.chain
    ) > 1:


        block_numbers = [

            block.index

            for block in (
                st.session_state.blockchain.chain
            )

            if block.index != 0
        ]


        selected_block = st.selectbox(
            "Select Patient Block",
            block_numbers
        )


        if st.button(
            "🔓 Decrypt Patient Record",
            use_container_width=True
        ):

            selected_block_data = (
                st.session_state.blockchain.chain[
                    selected_block
                ]
            )


            # --------------------------------------------
            # VERIFY BLOCKCHAIN
            # --------------------------------------------

            current_integrity = (
                st.session_state.blockchain.verify_chain()
            )


            if not current_integrity:

                st.error(
                    "🚨 TAMPER DETECTED! "
                    "Patient record cannot be safely accessed."
                )


            else:

                try:

                    decrypted_record = decrypt_data(
                        selected_block_data.encrypted_data,
                        st.session_state.aes_key
                    )


                    st.success(
                        "✅ Patient record decrypted successfully!"
                    )


                    st.subheader(
                        "🏥 Patient Record"
                    )


                    st.text(
                        decrypted_record
                    )


                except Exception:

                    st.error(
                        "❌ Unable to decrypt the record. "
                        "The data may have been tampered with."
                    )


    else:

        st.info(
            "No patient records available. "
            "Please secure a patient record first."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "🔐 EHR Blockchain Security | "
    "AES-256 • SHA-256 • Blockchain"
)