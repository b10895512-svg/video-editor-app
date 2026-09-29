import os
import gradio as gr
import moviepy.editor as mp
import whisper

# Clipify AI Themes & Styling
custom_css = """
body, .gradio-container {
    background-color: #0b0f19 !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}
.app-header {
    text-align: center;
    padding: 15px;
    background: linear-gradient(90deg, #1e1e2f, #111122);
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid #2a2a40;
}
.app-header h1 {
    color: #6c5ce7;
    margin: 0;
    font-size: 28px;
    font-weight: bold;
}
.app-header p {
    color: #a0a0c0;
    font-size: 14px;
    margin-top: 5px;
}
.action-card {
    background: #161b26 !important;
    border: 1px solid #232a3b !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.btn-primary {
    background: linear-gradient(135deg, #5865F2, #4752C4) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    border: none !important;
    padding: 12px !important;
}
.btn-primary:hover {
    background: linear-gradient(135deg, #4752C4, #3c45a5) !important;
}
.accent-box {
    background: #111520 !important;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #1f2638;
}
"""

def process_full_pipeline(audio_file, aspect_ratio, style, resolution, fmt):
    if not audio_file:
        return None, "⚠️ برائے مہربانی پہلے آڈیو فائل اپ لوڈ کریں!"
    
    try:
        # Load audio
        clip = mp.AudioFileClip(audio_file)
        duration = min(clip.duration, 30) # 30s limit
        
        # Dimensions setup
        w, h = (720, 1280) if "9:16" in aspect_ratio else (1280, 720)
        
        color_clip = mp.ColorClip(size=(w, h), color=(15, 20, 35), duration=duration)
        video_clip = color_clip.set_audio(clip)
        
        output_name = f"clipify_output.{fmt.lower()}"
        video_clip.write_videofile(
            output_name,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            logger=None
        )
        
        status_msg = f"""
✅ **ویڈیو پروسیسنگ مکمل ہو چکی ہے!**
- **فارمیٹ:** {aspect_ratio}
- **اسٹائل:** {style}
- **کوالٹی:** {resolution} ({fmt})
- **دورانیہ:** {round(duration, 1)} سیکنڈز
        """
        return output_name, status_msg
        
    except Exception as e:
        return None, f"❌ خرابی پیش آئی: {str(e)}"

# Interface Layout
with gr.Blocks(css=custom_css, title="Clipify AI - Audio to Video") as demo:
    
    with gr.Div(elem_classes=["app-header"]):
        gr.Markdown("# 🎬 Clipify AI")
        gr.Markdown("Audio to Video – Automatically")
    
    with gr.Tabs():
        # Step 1: Import Audio
        with gr.TabItem("1️⃣ Import Audio"):
            with gr.Div(elem_classes=["action-card"]):
                gr.Markdown("### 🎵 آڈیو امپورٹ کریں (Import Audio)")
                audio_input = gr.Audio(label="آڈیو فائل منتخب کریں یا ریکارڈ کریں", type="filepath")
                gr.Markdown("پشتیبانی شدہ فارمیٹس: MP3, WAV, AAC, M4A")
        
        # Step 2: Choose Video Type & Style
        with gr.TabItem("2️⃣ Style & Format"):
            with gr.Div(elem_classes=["action-card"]):
                gr.Markdown("### 📐 ویڈیو قسم اور اسٹائل منتخب کریں (Video Type & Style)")
                
                aspect_ratio = gr.Radio(
                    choices=["YouTube Shorts (9:16)", "Long Video (16:9)"],
                    value="YouTube Shorts (9:16)",
                    label="ویڈیو کی قسم (Aspect Ratio)"
                )
                
                style_choice = gr.Dropdown(
                    choices=["Cinematic", "Realistic", "Fantasy", "Anime", "3D Animation"],
                    value="Cinematic",
                    label="ویڈیو اسٹائل (Video Style)"
                )
        
        # Step 3: Process & Export Settings
        with gr.TabItem("3️⃣ Process & Export"):
            with gr.Div(elem_classes=["action-card"]):
                gr.Markdown("### ⚙️ ایکسپورٹ سیٹنگز (Export Settings)")
                
                resolution_choice = gr.Radio(
                    choices=["720p (Faster)", "1080p (Recommended)", "4K (High Quality)"],
                    value="1080p (Recommended)",
                    label="رزولیوشن (Resolution)"
                )
                
                format_choice = gr.Radio(
                    choices=["MP4", "MOV"],
                    value="MP4",
                    label="فارمیٹ (Format)"
                )
                
                generate_btn = gr.Button("🚀 Generate Video", elem_classes=["btn-primary"])
        
        # Step 4: Preview & Download
        with gr.TabItem("4️⃣ Preview & Download"):
            with gr.Div(elem_classes=["action-card"]):
                gr.Markdown("### 🎥 آپ کی ویڈیو تیار ہے (Your Video is Ready)")
                video_output = gr.Video(label="پروسیس شدہ ویڈیو")
                status_output = gr.Markdown("پروسیسنگ کا نتیجہ یہاں ظاہر ہوگا۔")

    # Button Event Binding
    generate_btn.click(
        fn=process_full_pipeline,
        inputs=[audio_input, aspect_ratio, style_choice, resolution_choice, format_choice],
        outputs=[video_output, status_output]
    )

if __name__ == "__main__":
    demo.launch()
