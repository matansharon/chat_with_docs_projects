from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='מערכת אוטומטית לתכנון ייצור', description='ברוכים הבאים למערכת האוטומטית לתכנון ייצור. כאן תוכלו לנהל את כל תהליכי הייצור בצורה יעילה וחכמה.')

if __name__ == '__main__':
    app.run(debug=True)
