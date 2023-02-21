from flask import Flask,make_response,url_for,redirect, request, render_template,current_app, g, send_file

print("hi")

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    a = 5
    return render_template('home.html',a = a)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",use_reloader=True,port=80)