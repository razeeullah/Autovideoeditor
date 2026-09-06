import os
import subprocess
import uuid
from flask import Flask, request, render_template, jsonify, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max-limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_audio_duration(file_path):
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-show_entries', 'format=duration', 
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        file_path
    ]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return float(output)
    except Exception as e:
        print(f"Error getting duration: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    if 'images' not in request.files or 'audio' not in request.files:
        return jsonify({'error': 'Images and audio are required'}), 400

    images = request.files.getlist('images')
    audio = request.files['audio']

    if not images or not audio.filename:
        return jsonify({'error': 'Images and audio are required'}), 400

    job_id = str(uuid.uuid4())
    job_dir = os.path.join(app.config['UPLOAD_FOLDER'], job_id)
    os.makedirs(job_dir, exist_ok=True)

    # Save audio
    audio_path = os.path.join(job_dir, f'audio_{audio.filename}')
    audio.save(audio_path)

    # Save images
    image_paths = []
    # Filter out empty files if any
    images = [img for img in images if img.filename]
    
    if len(images) == 0:
        return jsonify({'error': 'No valid images provided'}), 400

    for i, img in enumerate(images):
        ext = os.path.splitext(img.filename)[1] or '.jpg'
        img_path = os.path.join(job_dir, f'img_{i}{ext}')
        img.save(img_path)
        image_paths.append(img_path)

    audio_duration = get_audio_duration(audio_path)
    if not audio_duration:
         return jsonify({'error': 'Could not read audio file'}), 400

    # Calculate duration per image
    duration_per_image = audio_duration / len(image_paths)

    # Create ffmpeg concat file
    concat_file_path = os.path.join(job_dir, 'inputs.txt')
    with open(concat_file_path, 'w') as f:
        for img_path in image_paths:
            f.write(f"file '{os.path.abspath(img_path)}'\n")
            f.write(f"duration {duration_per_image:.3f}\n")
        # Add the last image again without duration as per ffmpeg concat demuxer quirks
        f.write(f"file '{os.path.abspath(image_paths[-1])}'\n")

    # Generate slideshow
    slideshow_path = os.path.join(job_dir, 'slideshow.mp4')
    ffmpeg_cmd_slideshow = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_file_path,
        '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        slideshow_path
    ]

    try:
        subprocess.run(ffmpeg_cmd_slideshow, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Error generating slideshow', 'details': str(e.stderr)}), 500

    # Mux with audio
    final_video_path = os.path.join(job_dir, 'final.mp4')
    ffmpeg_cmd_final = [
        'ffmpeg', '-y',
        '-i', slideshow_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        final_video_path
    ]

    try:
        subprocess.run(ffmpeg_cmd_final, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
         return jsonify({'error': 'Error mixing audio and video', 'details': str(e.stderr)}), 500

    return jsonify({'video_url': f'/download/{job_id}/final.mp4'})

@app.route('/download/<job_id>/<filename>')
def download(job_id, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], job_id), filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
