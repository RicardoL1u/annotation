from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
	return "Hello! This is the home page <h1>HELLO</h1>"

@app.route("/<name>")
def user(name):
	return f"Hello {name}!"

	# Now we when we go to /admin we will redirect to user with the argument "Admin!"
@app.route("/admin")
def admin():
	return redirect(url_for("user", name="Admin!"))  

if __name__ == "__main__":
	app.run()