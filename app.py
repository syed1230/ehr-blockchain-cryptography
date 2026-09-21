import streamlit as st

from crypto_utils import (
    generate_key,
    encrypt_data,
    decrypt_data,
    calculate_sha256
)

from blockchain import Blockchain


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EHR Blockchain Security",
    page_icon="🔐",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

if "aes_key" not in st.session_state:
    st.session_state.aes_key = generate_key()


# ============================================================
# HEADER
# ============================================================

st.title("🔐 EHR Blockchain Security System")

st.write(
    "A cryptographic security model for protecting "
    "Electronic Health Records using AES-256, SHA-256 and Blockchain."
)


# ============================================================
# SECURITY ARCHITECTURE
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔐 Encryption", "AES-256")

with col2:
    st.metric("🔑 Hashing", "SHA-256")

with col3:
    st.metric("⛓️ Storage", "Blockchain")

with col4:
    st.metric("🛡️ Security", "Verified")


st.divider()


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🏥 Patient Record",
        "⛓️ Blockchain",
        "🛡️ Security",
        "🔓 Authorized Access"
    ]
)


# ============================================================
# TAB 1 — PATIENT RECORD
# ============================================================

with tab1:

    st.header("🏥 Secure Patient Record")

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

        if patient_name and patient_id and diagnosis:

            # Create patient record
            patient_record = (
                f"Name: {patient_name}\n"
                f"Patient ID: {patient_id}\n"
                f"Age: {age}\n"
                f"Blood Group: {blood_group}\n"
                f"Diagnosis: {diagnosis}"
            )

            # AES-256 encryption
            encrypted_data = encrypt_data(
                patient_record,
                st.session_state.aes_key
            )

            # SHA-256 hash
            data_hash = calculate_sha256(
                encrypted_data
            )

            # Add record to blockchain
            st.session_state.blockchain.add_block(
                encrypted_data,
                data_hash
            )

            st.success(
                "✅ Patient record secured successfully!"
            )

            st.subheader(
                "🔐 AES-256 Encrypted Data"
            )

            st.code(
                encrypted_data
            )

            st.subheader(
                "🔑 SHA-256 Hash"
            )

            st.code(
                data_hash
            )

        else:

            st.warning(
                "Please fill in all required fields."
            )


# ============================================================
# TAB 2 — BLOCKCHAIN
# ============================================================

with tab2:

    st.header("⛓️ Blockchain")

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

            # Show encrypted data only for patient blocks
            if block.index != 0:

                st.write(
                    "**Encrypted Patient Data:**"
                )

                st.code(
                    block.encrypted_data
                )


# ============================================================
# TAB 3 — SECURITY
# ============================================================

with tab3:

    st.header(
        "🛡️ Blockchain Security"
    )

    st.write(
        "Verify blockchain integrity or simulate "
        "a tampering attack."
    )

    # --------------------------------------------------------
    # BLOCKCHAIN VERIFICATION
    # --------------------------------------------------------

    st.subheader(
        "🔍 Integrity Verification"
    )

    if st.button(
        "🔍 Verify Blockchain",
        use_container_width=True
    ):

        is_valid = (
            st.session_state.blockchain.verify_chain()
        )

        if is_valid:

            st.success(
                "✅ Blockchain is valid. "
                "No tampering detected."
            )

        else:

            st.error(
                "🚨 TAMPER DETECTED! "
                "Blockchain integrity has been compromised."
            )

    st.divider()

    # --------------------------------------------------------
    # TAMPERING SIMULATION
    # --------------------------------------------------------

    st.subheader(
        "⚠️ Tampering Simulation"
    )

    st.write(
        "This feature intentionally modifies a blockchain "
        "record to demonstrate tamper detection."
    )

    if st.button(
        "💥 Simulate Tampering",
        use_container_width=True
    ):

        if len(
            st.session_state.blockchain.chain
        ) > 1:

            tampered_block = (
                st.session_state.blockchain.chain[1]
            )

            tampered_block.encrypted_data += (
                "TAMPERED"
            )

            st.warning(
                "⚠️ Block 1 has been modified!"
            )

            st.write(
                "The blockchain data was intentionally "
                "changed to simulate an attack."
            )

        else:

            st.info(
                "Please secure at least one patient "
                "record first."
            )


# ============================================================
# TAB 4 — AUTHORIZED ACCESS
# ============================================================

with tab4:

    st.header(
        "🔓 Authorized Patient Record Access"
    )

    st.write(
        "Authorized users can decrypt a stored patient "
        "record using the AES-256 key."
    )

    if len(
        st.session_state.blockchain.chain
    ) > 1:

        block_numbers = [
            block.index
            for block in st.session_state.blockchain.chain
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