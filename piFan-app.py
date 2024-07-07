from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from crontab import CronTab
import random
import calendar
import re
import subprocess

piFan = Flask(__name__)
piFan.static_folder = 'static'
load_dotenv()

@piFan.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@piFan.route('/schedule', methods=['POST'])
def schedule():
    minute = request.form['minute']
    hour = request.form['hour']
    day_of_month = request.form['day_of_month']
    month = request.form['month']
    day_of_week = request.form['day_of_week']
    command_arg = request.form['command']
    id = random.randint(0, 999999)

    command = f"python3 /home/pi/git/piFan/scripts/piFan.py -action {command_arg}"

    add_cron(minute,hour,day_of_month,month,day_of_week,command,id)
  
    return render_template('index.html')

@piFan.route('/jobs')
def jobs():
    jobs = list_cron()
    return render_template('jobs.html', jobs=jobs)

@piFan.route('/delete_job/<job_id>', methods=['POST'])
def delete_job(job_id):
    del_cron(job_id)
    return redirect(url_for('jobs'))

@piFan.route('/remote/<argument>', methods=['POST'])
def remote_control(argument):
    script_path = "/home/pi/git/piFan/scripts/piFan.py"
    try:
        result = subprocess.run(["python3", script_path, '-action', argument], capture_output=True, text=True, check=True)
        return f"<pre>{result.stdout}</pre>"
    except subprocess.CalledProcessError as e:
        return f"<pre>Error: {e.stderr}</pre>"

# Create Cron job
def add_cron(minute, hour, day_of_month, month, day_of_week, command, id):
    cron = CronTab(user=True)
    job = cron.new(command=f"{command}", comment=f"id={id}")
    cron_config = f"{minute} {hour} {day_of_month} {month} {day_of_week}"
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

        job_id_pattern = r'\b\d{6}\b'
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
    piFan.run(debug=True, host='0.0.0.0', port=5500)