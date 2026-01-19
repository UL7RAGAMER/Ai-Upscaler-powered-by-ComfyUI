
## 🚀 Setup Instructions

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/UL7RAGAMER/Ai-Upscaler-powered-by-ComfyUI.git
cd Ai-Upscaler-powered-by-ComfyUI

```

### 2. Prepare the ComfyUI Environment

1. **Download:** Get the latest version: **[Download ComfyUI Windows Portable](https://www.google.com/search?q=https://github.com/comfyanonymous/ComfyUI/releases/latest/download/ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z)**.
2. **Extract & Place:** Move the folder named `ComfyUI_windows_portable` into the root of this project.
3. **Update:** Navigate to `ComfyUI_windows_portable/update/` and run:
* **`update_comfyui_and_python_dependencies.bat`**



### 3. Install Manager and Model Downloader

1. **Install ComfyUI Manager:** Open your terminal in `ComfyUI_windows_portable/ComfyUI/custom_nodes/` and run:
```bash
git clone https://github.com/ltdrdata/ComfyUI-Manager.git

```


2. **Install Workflow Models Downloader:** Launch ComfyUI (using `run_nvidia_gpu.bat`). Click the **Manager** button, go to **"Install Custom Nodes"**, and search for:
* `https://github.com/slahiri/ComfyUI-Workflow-Models-Downloader`



### 4. Download Models & Optimize Environment

Once the tools above are installed:

1. Open the ComfyUI Web Interface.
2. Locate the **Model Download** button (from the Downloader node) and click it to fetch the required upscaler models.
3. **Install SageAttention & Streamlit:** Once the models are downloaded, close ComfyUI and run the following commands in your terminal to optimize performance and install the UI framework:
```bash
# Install SageAttention for faster processing
./ComfyUI_windows_portable/python_embeded/python.exe -m pip install "https://huggingface.co/Wildminder/AI-windows-whl/resolve/main/sageattention-2.2.0.post3%2Bcu130torch2.10.0-cp313-cp313-win_amd64.whl?download=true"

# Install Streamlit
./ComfyUI_windows_portable/python_embeded/python.exe -m pip install streamlit

```



---

## 🛠 Usage

To launch the streamlined AI Upscaler interface, run the following command from the project root:

```bash
./ComfyUI_windows_portable/python_embeded/python.exe -m streamlit run main.py

```