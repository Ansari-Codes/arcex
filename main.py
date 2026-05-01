from app import app, routate
from Pages.home import HomePage

routate(HomePage)

app.run(debug=True, port=9000)
