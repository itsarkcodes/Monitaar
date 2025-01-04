from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Website
from forms import WebsiteForm
from threading import Thread
import monitor
import os
from dotenv import load_dotenv
from flask_migrate import Migrate  # Import Migrate

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///websites.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Migrate

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    websites = Website.query.all()
    return render_template('index.html', websites=websites)

@app.route('/add', methods=['GET', 'POST'])
def add_website():
    form = WebsiteForm()
    if form.validate_on_submit():
        website = Website(
            url=form.url.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            slack_user_ids=form.slack_user_ids.data,
            tag_here=form.tag_here.data  # New field
        )
        db.session.add(website)
        db.session.commit()
        flash('Website added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_website.html', form=form)

@app.route('/edit/<int:website_id>', methods=['GET', 'POST'])
def edit_website(website_id):
    website = Website.query.get_or_404(website_id)
    form = WebsiteForm(obj=website)
    if form.validate_on_submit():
        website.url = form.url.data
        website.start_time = form.start_time.data
        website.end_time = form.end_time.data
        website.slack_user_ids = form.slack_user_ids.data
        website.tag_here = form.tag_here.data  # Update the field
        db.session.commit()
        flash('Website updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_website.html', form=form, website=website)

@app.route('/delete/<int:website_id>', methods=['POST'])
def delete_website(website_id):
    website = Website.query.get_or_404(website_id)
    db.session.delete(website)
    db.session.commit()
    flash('Website deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Start the monitoring in a separate thread
    monitor_thread = Thread(target=monitor.start_monitoring, args=(app,))
    monitor_thread.daemon = True
    monitor_thread.start()
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
