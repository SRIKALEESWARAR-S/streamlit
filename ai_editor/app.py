
import streamlit as st
import os
import asyncio
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip

# Streamlit UI
st.title("🎬 Jolly AI Voice - Video Generator")
st.write("உங்களுடைய ஸ்கிரிப்ட் மற்றும் புகைப்படங்களை கொடுத்தால் தானாக வீடியோ உருவாகும்!")

# 1. Script Input
script_input = st.text_area("கதை அல்லது விழிப்புணர்வு ஸ்கிரிப்ட் (Tamil)", height=150, 
                            placeholder="இங்கே உங்கள் ஸ்கிரிப்டை டைப் செய்யவும்...")

# 2. Audio Settings
voice_option = st.selectbox("AI குரல் தேர்வு செய்க:", 
                            ["ta-IN-PallaviNeural (Female)", "ta-IN-ValluvarNeural (Male)"])
voice_id = voice_option.split(" ")[0]

# 3. Image Upload (Upto 25 photos)
uploaded_files = st.file_uploader("புகைப்படங்களை அப்லோட் செய்யவும் (அதிகபட்சம் 25):", 
                                  type=["jpg", "jpeg", "png"], 
                                  accept_multiple_files=True)

if uploaded_files and len(uploaded_files) > 25:
    st.error("⚠️ தயவுசெய்து 25 புகைப்படங்களுக்கு மிகாமல் அப்லோட் செய்யவும்.")

# 4. Background Music Upload (Optional)
bg_music_file = st.file_uploader("பின்னணி இசை (Background Music - Optional):", type=["mp3", "wav"])

# Async function for Microsoft Edge TTS
async def generate_voice(text, voice, output_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

# Video Generation Logic
if st.button("🚀 வீடியோவை உருவாக்கு"):
    if not script_input:
        st.warning("⚠️ தயவுசெய்து முதலில் ஸ்கிரிப்ட் எழுதவும்.")
    elif not uploaded_files:
        st.warning("⚠️ வீடியோவிற்கு தேவையான புகைப்படங்களை அப்லோட் செய்யவும்.")
    else:
        with st.spinner("குரல் மற்றும் வீடியோ உருவாக்கப்படுகிறது... சற்றே காத்திருக்கவும்..."):
            try:
                # Temporary file paths
                voice_audio_path = "voiceover.mp3"
                final_video_path = "final_output.mp4"
                
                # Step 1: Generate AI Voice
                asyncio.run(generate_voice(script_input, voice_id, voice_audio_path))
                
                # Load voice audio to calculate duration
                voice_audio = AudioFileClip(voice_audio_path)
                total_duration = voice_audio.duration
                
                # Step 2: Process Images & Calculate Duration per image
                num_images = len(uploaded_files)
                duration_per_image = total_duration / num_images
                
                clips = []
                # Save uploaded files temporarily and create image clips
                for i, file in enumerate(uploaded_files):
                    temp_img_path = f"temp_img_{i}.png"
                    with open(temp_img_path, "wb") as f:
                        f.write(file.getbuffer())
                    
                    # Create individual image clip
                    img_clip = ImageClip(temp_img_path).set_duration(duration_per_image)
                    clips.append(img_clip)
                
                # Concatenate all image clips into one video
                video_track = concatenate_videoclips(clips, method="compose")
                
                # Step 3: Handle Background Music
                if bg_music_file:
                    bg_music_path = "bg_music.mp3"
                    with open(bg_music_path, "wb") as f:
                        f.write(bg_music_file.getbuffer())
                    
                    bg_audio = AudioFileClip(bg_music_path).volumex(0.15) # Reduce BG music volume to 15%
                    bg_audio = bg_audio.loop(duration=total_duration) # Loop music to fit video
                    
                    # Mix voiceover and background music
                    final_audio = CompositeAudioClip([voice_audio, bg_audio])
                else:
                    final_audio = voice_audio
                
                # Step 4: Set Audio to Video and Export
                final_video = video_track.set_audio(final_audio)
                
                # Write file to cloud storage (fps 24 is good for YouTube shorts/videos)
                final_video.write_videofile(final_video_path, fps=24, codec="libx264", audio_codec="aac")
                
                # Close clips to free memory
                final_video.close()
                voice_audio.close()
                
                # Clean up temporary image files
                for i in range(num_images):
                    if os.path.exists(f"temp_img_{i}.png"):
                        os.remove(f"temp_img_{i}.png")
                if os.path.exists(voice_audio_path): os.remove(voice_audio_path)
                if bg_music_file and os.path.exists("bg_music.mp3"): os.remove("bg_music.mp3")
                
                st.success("🎉 வீடியோ வெற்றிகரமாக உருவாக்கப்பட்டது!")
                
                # Display and Download Option
                with open(final_video_path, "rb") as video_file:
                    st.video(video_file.read())
                    st.download_button(label="📥 வீடியோவை டவுன்லோட் செய்யுங்க", data=video_file, file_name="jolly_ai_video.mp4", mime="video/mp4")

            except Exception as e:
                st.error(f"❌ ஏதோ தவறு நடந்துவிட்டது: {str(e)}")

