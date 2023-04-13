from flask import Flask, render_template, request,redirect, url_for
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/redirect-to-index')
def redirect_to_index():
    return redirect(url_for('index'))

@app.route('/aboutus.html')
def aboutus():
    return render_template('aboutus.html')

# @app.route('/index.html')
# def redirect_to_aboutus():
#     return redirect(url_for('about.html'))

@app.route('/contactus.html')
def contactus():
    return render_template('contactus.html')

# @app.route('/redirect')
# def redirect_to_aboutus():
#     return redirect(url_for('contactus.html'))

@app.route('/privacypolicy.html')
def privacypolicy():
    return render_template('privacypolicy.html')

# @app.route('/redirect')
# def redirect_to_aboutus():
#     return redirect(url_for('privacypolicy.html'))


@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']

    response = requests.get(video_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    script = soup.find('script', {'id': '__PWS_DATA__', 'type': 'application/json'})
    if script is None:
        return render_template('error.html', message='Cannot find script tag')

    data = json.loads(script.string)

    # Extract video URL from JSON data
    try:
        video_data = data['props']['initialReduxState']['pins'][list(data['props']['initialReduxState']['pins'].keys())[0]]['videos']['video_list']['V_720P']['url']
    except KeyError:
        return render_template('error.html', message='Cannot find video URL')

    video_url = video_data

    # Download video
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(video_url, headers=headers)

    # with open('video.mp4', 'wb') as f:
    #     f.write(response.content)

    return redirect(video_data, code=302)

if __name__ == '__main__':
    app.run(debug=True)
