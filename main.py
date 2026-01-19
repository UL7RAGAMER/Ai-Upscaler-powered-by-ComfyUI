import os
import streamlit as st
import requests
import json
import websocket
import uuid
from PIL import Image
import io

# --- CONFIGURATION ---
COMFY_ADDRESS = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())

# --- THEME & DESIGN ---
def set_design():
    st.set_page_config(page_title="AI Upscaler Pro", layout="wide")
    st.markdown("""
        <style>
        /* Main background and text */
        .stApp {
            background-color: #0A192F;
            color: #E6F1FF;
        }
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #112240 !important;
            border-right: 1px solid #233554;
        }
        /* Title styling */
        h1 {
            color: #CCD6F6;
            font-weight: 800 !important;
            letter-spacing: -1px;
        }
        /* Highlight Color (Yellow) */
        .yellow-text {
            color: #FACC15;
        }
        /* Primary Button (Blue) */
        div.stButton > button:first-child {
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #FACC15;
            color: #0A192F;
            transform: translateY(-2px);
        }
        /* Status boxes */
        div[data-testid="stStatusWidget"] {
            background-color: #112240;
            border: 1px solid #FACC15;
        }
        </style>
    """, unsafe_allow_html=True)

set_design()

st.markdown('<h1>✨ <span class="yellow-text">AI</span> Upscaler Pro</h1>', unsafe_allow_html=True)
st.divider()

# --- UI LAYOUT ---
with st.sidebar:
    st.markdown('<h2 class="yellow-text">Source Image</h2>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your file below", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Input Preview", use_container_width=True)

# Main area layout with better spacing
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.info("💡 **Tip:** Ensure ComfyUI is running on port 8188 before starting.")
    process_btn = st.button("🚀 GET OUTPUT", type="primary", use_container_width=True)

# --- LOGIC ---
if process_btn and uploaded_file:
    with col2: 
        with st.status("🔮 Neural Processing...", expanded=True) as status:
            # 1. Upload
            files = {"image": (uploaded_file.name, uploaded_file.getvalue())}
            resp = requests.post(f"http://{COMFY_ADDRESS}/upload/image", files=files)
            server_filename = resp.json()["name"]
            
            # 2. Load & Find Node
            script_dir = os.path.dirname(os.path.abspath(__file__))
            workflow_path = os.path.join(script_dir, "workflow_api.json")
            with open(workflow_path, "r") as f:
                workflow = json.load(f)
            
            for node_id, node_data in workflow.items():
                if node_data.get("class_type") == "LoadImage":
                    workflow[node_id]["inputs"]["image"] = server_filename
                    break

            # 3. Queue
            p = {"prompt": workflow, "client_id": CLIENT_ID}
            data = json.dumps(p).encode('utf-8')
            requests.post(f"http://{COMFY_ADDRESS}/prompt", data=data)
            
            # 4. WebSocket
            ws = websocket.create_connection(f"ws://{COMFY_ADDRESS}/ws?clientId={CLIENT_ID}")
            output_images = []

            while True:
                out = ws.recv()
                if isinstance(out, str):
                    message = json.loads(out)
                    if message['type'] == 'executed':
                        if 'images' in message['data']['output']:
                            for img_data in message['data']['output']['images']:
                                output_images.append(img_data)
                    if message['type'] == 'executing' and message['data']['node'] is None:
                        break 
            
            # 5. Result Fetching
            if output_images:
                img_info = output_images[-1]
                view_url = f"http://{COMFY_ADDRESS}/view?filename={img_info['filename']}&subfolder={img_info['subfolder']}&type={img_info['type']}"
                img_response = requests.get(view_url)
                
                if img_response.status_code == 200:
                    output_image = Image.open(io.BytesIO(img_response.content))
                    st.success("Success!")
                    st.image(output_image, caption="Enhanced Result", use_container_width=True)
                else:
                    st.error("Retrieval failed.")
            else:
                st.warning("No output detected.")