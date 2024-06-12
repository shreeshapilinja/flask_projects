import os
from flask import Flask, request, render_template, send_file
from pytube import YouTube

os.makedirs('downloads', exist_ok=True)

app = Flask(__name__)

def clear_download_folder():
    folder = 'downloads'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

@app.route('/', methods=['GET', 'POST'])
def home():
    url = None
    format_choice = 'mp3'  # Default format is MP3
    error_message = None

    if request.method == 'POST':
        url = request.form['url']
        format_choice = request.form.get('format', 'mp3')

    if not url:
        url = request.args.get('url')
        format_choice = request.args.get('format', 'mp3')

    if not url:
        return render_template('index.html', error_message='')

    try:
        clear_download_folder()  
        yt = YouTube(url)

        if format_choice == 'mp3':
            stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            filename = f"{yt.title}.mp3"
        elif format_choice == 'wav':
            stream = yt.streams.filter(only_audio=True, file_extension='webm').first()
            filename = f"{yt.title}.wav"
        elif format_choice == 'webm_audio':
            stream = yt.streams.filter(only_audio=True, file_extension='webm').first()
            filename = f"{yt.title}.webm"
        elif format_choice == 'webm':
            stream = yt.streams.get_highest_resolution()
            filename = f"{yt.title}.webm"
        else:
            stream = yt.streams.get_highest_resolution()
            filename = f"{yt.title}.mp4"

        if stream:
            stream.download(output_path='downloads', filename=filename)
            return send_file(f'downloads/{filename}', as_attachment=True)
        else:
            error_message = "No suitable stream found for the selected format."
    except Exception as e:
        error_message = str(e)

    return render_template('index.html', error_message=error_message)

if __name__ == '__main__':
    app.run()
