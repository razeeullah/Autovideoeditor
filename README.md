<h1 align="center">🤖 AutoVidEditor</h1>

<p align="center">
  <strong>An automated AI video editing application that does your entire editing work for you!</strong>
</p>

---

## 🚀 What is this?

**AutoVidEditor** is a modern, lightweight web application built with Python (Flask). It takes the hassle out of video editing. If you have a voiceover and a set of images, this AI tool will automatically sync them together on a timeline, calculate the perfect durations, and generate a final 1080p high-quality video for you. 

*Just add your images, add your voiceover, and click generate!*

## ✨ Features

- 🎨 **Modern Interface:** A sleek, dark-mode glassmorphism UI.
- ⏱️ **Auto-Sync Timeline:** Automatically calculates the length of your voiceover and spaces your images perfectly.
- 🎬 **FFmpeg Powered:** Leverages the industry-standard `ffmpeg` for lightning-fast, high-quality (1080p) video rendering.
- ☁️ **Cloud Ready:** Comes pre-configured with Docker, ready to be deployed to Render.com with a single click.

---

## 🛠️ How to Use It

1. **Upload Images:** Select your sequence of images (JPG, PNG).
2. **Upload Audio:** Select your voiceover track (MP3, WAV).
3. **Generate:** Click the 'Generate Video' button. 
4. **Download:** The AI will stitch everything together step-by-step according to the timeline. Download your final video instantly!

---

## 💻 Local Installation

If you want to run this tool on your own computer, follow these simple steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Autovideoeditor.git
   cd Autovideoeditor/AutoVidEditor
   ```

2. **Set up Python environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   *Then open your browser and go to `http://localhost:5000`*

*(Note: You must have [ffmpeg](https://ffmpeg.org/download.html) installed on your system to run this locally).*

---

## ☁️ Deploy to Render.com (Recommended)

You can host this tool online for free using Render!

1. Fork or push this repository to your GitHub account.
2. Go to [Render.com](https://render.com) and click **New Web Service**.
3. Connect your GitHub account and select this repository.
4. Render will automatically detect the `Dockerfile`, install `ffmpeg`, and launch your app.
5. Set the Root Directory to `AutoVidEditor`.
6. Click Deploy!

---

*Resources and tutorials mentioned in the video are built into this repository. Enjoy automated editing!*
