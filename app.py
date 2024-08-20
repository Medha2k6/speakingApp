from flask import Flask, request, send_file, render_template
import boto3
import io

app = Flask(__name__)

# Initialize the Polly client
polly_client = boto3.client('polly')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize_speech():
    text = request.form.get('text')
    if not text:
        return "Text is required", 400
    
    response = polly_client.synthesize_speech(
        VoiceId='Matthew',
        OutputFormat='mp3',
        Text=text
    )

    # Read the audio stream from the response
    audio_stream = response['AudioStream'].read()

    # Create a BytesIO buffer and save the audio stream
    buffer = io.BytesIO(audio_stream)
    buffer.seek(0)

    # Return the audio file as an attachment
    return send_file(
        buffer,
        as_attachment=True,
        download_name='output.mp3',
        mimetype='audio/mp3'
    )

if __name__ == "__main__":
    app.run(debug=True)
