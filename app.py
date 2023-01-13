from flask import Flask, render_template, Response, request

from stream import gen_frames

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    param_url = request.args.get('param_url')
    # param_url = 'https://www.youtube.com/watch?v=38hnIitudak&ab_channel=ViralFACTORY'
    # print(param_url)
    return Response(gen_frames(param_url), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/test')
def test_index():
    """Video streaming home page."""
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)