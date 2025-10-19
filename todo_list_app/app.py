# todo_list_app/app.py - CORRECTED

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

# Initialize the Flask application
app = Flask(__name__)

# JINJA CONTEXT PROCESSOR: This makes the 'datetime' object
# available to ALL your templates (index.html, future.html, etc.)
@app.context_processor
def inject_datetime():
    """Makes datetime available in all Jinja templates to solve the UndefinedError."""
    # We also inject timedelta for good measure, though not strictly required by the current code
    return {'datetime': datetime, 'timedelta': timedelta}

# Task Storage: A dictionary to store tasks.
# Key: Date string (YYYY-MM-DD)
# Value: List of dictionaries (e.g., [{'time': '14:30', 'task': 'Meeting', 'id': 1}])
TASKS = {}
task_id_counter = 1

def add_task_to_storage(date, time, task):
    """Adds a new task to the global TASKS dictionary and sorts the list by time."""
    global task_id_counter
    
    # Check if the date key exists, if not, create it
    if date not in TASKS:
        TASKS[date] = []
        
    # Create the new task dictionary
    new_task = {
        'id': task_id_counter,
        'time': time,
        'task': task
    }
    
    # Add task
    TASKS[date].append(new_task)
    task_id_counter += 1
    
    # Sort the tasks for this date by time
    TASKS[date].sort(key=lambda item: item['time'])

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles the main page: Adding tasks and viewing today's tasks."""
    today_str = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        # 1. Handle Task Addition
        task = request.form.get('task')
        date_str = request.form.get('date')
        time = request.form.get('time')

        if task and date_str and time:
            add_task_to_storage(date_str, time, task)
            # Redirect to GET request to clear form data
            return redirect(url_for('index'))

    # 2. Handle Task Deletion (via query parameter on GET request)
    task_id_to_delete = request.args.get('delete_id', type=int)
    delete_date = request.args.get('date', type=str)
    
    if task_id_to_delete and delete_date in TASKS:
        # Find and remove the task
        TASKS[delete_date] = [t for t in TASKS[delete_date] if t['id'] != task_id_to_delete]
        
        # Clean up the dictionary if the date is now empty
        if not TASKS[delete_date]:
            del TASKS[delete_date]
            
        return redirect(url_for('index'))

    # 3. View Today's Tasks
    today_tasks = TASKS.get(today_str, [])
    
    # Removed: datetime=datetime (Context Processor handles this now)
    return render_template(
        'index.html',
        today_str=today_str,
        today_tasks=today_tasks
    )

@app.route('/future')
def future():
    """Handles the future page: Viewing upcoming 10 days of tasks."""
    
    today = datetime.now().date()
    future_tasks = {}

    # Calculate the next 10 days (including today)
    for i in range(10):
        current_date = today + timedelta(days=i)
        current_date_str = current_date.strftime('%Y-%m-%d')
        
        # Check if we have tasks for this date
        if current_date_str in TASKS:
            future_tasks[current_date_str] = {
                # Note: No need for 'datetime' here, the calculation is done in Python
                'display_date': current_date.strftime('%A, %B %d'),
                'tasks': TASKS[current_date_str]
            }

    # Removed: datetime=datetime (Context Processor handles this now)
    return render_template('future.html', future_tasks=future_tasks)


if __name__ == '__main__':
    # Add a sample task for testing
    add_task_to_storage(datetime.now().strftime('%Y-%m-%d'), '10:00', 'Finish Project 2 Code')
    
    # Add a future sample task
    future_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    add_task_to_storage(future_date, '08:30', 'Schedule Dentist Appointment')
    
    app.run(host='0.0.0.0', debug=True)