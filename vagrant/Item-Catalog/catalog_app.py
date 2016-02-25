from catalog import app

app.secret_key = 'secret_key'
app.run(host='0.0.0.0', port=8000, debug=True)


