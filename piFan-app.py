from flask import Flask, render_template, jsonify, request, redirect, url_for
from dotenv import load_dotenv
from crontab import CronTab
import random
import calendar
from datetime import datetime
import re
import subprocess
from dotenv import load_dotenv
import os

piFan = Flask(__name__)
piFan.static_folder = 'static'
load_dotenv()
try:
    location = os.environ.get('location')
    cert = os.environ.get("cert")
    key = os.environ.get("key")
except:
    print("Make sure the environment variables are defined.")

@piFan.route('/manifest.json')
def manifest():
    manifest_data = {
        "name": "piFan",
        "short_name": "piFan",
        "description": "piFan web app",
        "start_url": "./templates/index.html",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#000000",
        "icons": [
            {
                "src": "/static/img/icon_64.png",
                "type": "image/png",
                "sizes": "64x64",
                "purpose": "any maskable"
            },
            {
                "src": "/static/img/icon_128.png",
                "type": "image/png",
                "sizes": "128x128",
                "purpose": "any maskable"
            },
            {
                "src": "/static/img/icon_512.png",
                "type": "image/png",
                "sizes": "512x512",
                "purpose": "any maskable"
            }
        ]   
    }
    
    return jsonify(manifest_data)

@piFan.route('/', methods=['GET', 'POST'])
def index():
    jobs = list_cron()
    return render_template('index.html', jobs=jobs)

@piFan.route('/schedule', methods=['POST'])
def schedule():

    # Simple Date Config
    if 'date_complete' in request.form and 'time_complete' in request.form:
        date = request.form['date_complete']
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        weekday = date_obj.strftime('%A')
        weekday_number = date_obj.weekday()
        
        time = request.form['time_complete']
        time_obj = datetime.strptime(time, '%H:%M')
        hour = time_obj.hour
        minute = time_obj.minute
    else:        
        # Advanced Date Config
        minute = request.form['minute']
        hour = request.form['hour']
        day = request.form['day_of_month']
        month = request.form['month']
        weekday_number = request.form['day_of_week']
        id = random.randint(0, 999999)
        
    # Common config
    command_arg = request.form['command']
    id = random.randint(0, 999999)
    command = f"python3 {location}/scripts/piFan.py -action {command_arg}"
    add_cron(minute,hour,day,month,weekday_number,command,id)

    if 'date_complete' in request.form:
        return redirect(url_for('index') + '#simple')
    else:
        return redirect(url_for('index') + '#advanced')


@piFan.route('/jobs')
def jobs():
    jobs = list_cron()
    return render_template('jobs.html', jobs=jobs)

@piFan.route('/delete_job/<job_id>', methods=['POST'])
def delete_job(job_id):
    del_cron(job_id)
    jobs = list_cron()
    return redirect(url_for('index'))

@piFan.route('/remote', methods=['GET', 'POST'])
def remote():
    if request.method == 'POST':
        action = request.form.get('action')
        execute_script(action)
        return redirect(url_for('index') + '#remote')
    return render_template('remote.html')
    #return redirect(url_for('index'))

### ACTIONS ###

# Execute script
def execute_script(action):
    script = f'{location}/scripts/piFan.py'
    command = f'python3 {script} -action {action}'
    subprocess.run(command, shell=True)

# Create Cron job
def add_cron(minute, hour, day, month, weekday, command, id):
    cron = CronTab(user=True)
    job = cron.new(command=f"{command}", comment=f"id={id}")
    cron_config = f"{minute} {hour} {day} {month} {weekday}"
    job.setall(cron_config)
    cron.write()

# Delete Cron jobs
def del_cron(id):
    cron = CronTab(user=True)
    job_to_delete = None

    for job in cron:
        if id in job.comment:
            job_to_delete = job
            break

    if job_to_delete:
        cron.remove(job_to_delete)
        cron.write()
        print(f"Job with id '{id}' deleted.")
    else:
        print(f"No job with id '{id}' found.")

# List Cron jobs
def list_cron():
    cron = CronTab(user=True)
    jobs = []
    jobs_list = []

    for job in cron:
        jobs.append(job)

    for index, job in enumerate(jobs, start=1):
        minute = job.minute.render()
        hour = job.hour.render()
        day_of_month = job.dom.render()
        month = job.month.render()
        day_of_week = job.dow.render()
        
        day_of_week_name = get_weekday_name(day_of_week)
        month_name = get_month_name(month)

        job_command_pattern = r'(?<=action\s).*'
        job_command = re.findall(job_command_pattern, job.command)

        job_id_pattern = r'\b\d{1,6}\b'
        job_id = re.findall(job_id_pattern, job.comment)

        job_dict = {
            "Job Index": index,
            "Job ID": job_id[0],
            "Day of Week": day_of_week_name,
            "Day of Month": day_of_month,
            "Month": month_name,
            "Hour": hour,
            "Minute": minute,
            "Command": job_command[0]
        }
        
        jobs_list.append(job_dict)
    
    return jobs_list

# Name of the day of the week
def get_weekday_name(day_of_week):
    try:
        day_index = int(day_of_week)
        return calendar.day_name[day_index]
    except (ValueError, IndexError):
        return day_of_week 

# Name of the month
def get_month_name(month):
    try:
        month_index = int(month)
        return calendar.month_name[month_index]
    except (ValueError, IndexError):
        return month

if __name__ == '__main__':
    piFan.run(ssl_context=(cert, key), debug=True, host='0.0.0.0', port=5500)