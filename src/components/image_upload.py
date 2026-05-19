"""
Optional medical image upload for multimodal diagnosis (Phase 2C).
"""

from typing import Any, Dict, Optional, Tuple

import streamlit as st

MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]


def render_image_upload(translations: Dict[str, Any]) -> Tuple[Optional[bytes], Optional[str], Optional[str]]:
    """
    Render optional image uploader and type selector.

    Returns:
        Tuple of (image_bytes, mime_type, image_type_label) or Nones if no upload
    """
    trans = translations
    st.markdown(f"**{trans.get('imaging_header', 'Medical image (optional)')}**")
    st.caption(trans.get("imaging_consent", "Images are not stored. For educational use only."))

    image_type = st.selectbox(
        trans.get("imaging_type_label", "Image type"),
        options=[
            trans.get("imaging_type_skin", "Skin / rash"),
            trans.get("imaging_type_xray", "X-ray"),
            trans.get("imaging_type_ecg", "ECG trace"),
            trans.get("imaging_type_lab", "Lab report photo"),
            trans.get("imaging_type_other", "Other"),
        ],
        key="mdx_image_type",
    )

    uploaded = st.file_uploader(
        trans.get("imaging_upload_label", "Upload image (JPG/PNG, max 5 MB)"),
        type=["jpg", "jpeg", "png"],
        key="mdx_medical_image",
    )

    if uploaded is None:
        return None, None, None

    data = uploaded.getvalue()
    if len(data) > MAX_IMAGE_BYTES:
        st.error(trans.get("imaging_too_large", "Image exceeds 5 MB limit."))
        return None, None, None

    mime = uploaded.type or "image/jpeg"
    if mime not in ALLOWED_TYPES and mime != "image/jpg":
        st.warning(trans.get("imaging_type_warning", "Use JPG or PNG format."))
        mime = "image/jpeg"

    return data, mime, image_type
