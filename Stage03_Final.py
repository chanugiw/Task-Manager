#Author:Chanugi Weerakoon
#Date:13th April 2025
#Task Manager

import json
#List to store tasks
tasks = []

FILE_NAME="tasks.json"

# Function to validate task priority
def validate_priority(priority):
    # Check if the priority is one of the valid values: High, Medium, Low
    return priority.lower() in ["high", "medium", "low"]

# Simple function to validate date format without datetime module
def validate_date(date):
    try:
        # Check format YYYY-MM-DD
        if len(date) != 10 or date[4] != '-' or date[7] != '-':
            return False
            
        # Extract year, month, day
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        
        # Basic validation
        if year < 1900 or year > 2100:
            return False
        if month < 1 or month > 12:
            return False
            
        # Check day based on month
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # Adjust February for leap years
        if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
            days_in_month[2] = 29
            
        if day < 1 or day > days_in_month[month]:
            return False
            
        return True
    except (ValueError, IndexError):
        return False



#Function to add a task
def add_task():
    task_name = input("Enter task name: ")
    task_description = input("Enter task description: ")
    task_priority = input("Enter task priority(High/Medium/Low): ")
    
    # Validate task priority input
    while not validate_priority(task_priority):
       task_priority = input("Enter task priority(High/Medium/Low): ")
    
     # Validate due_date input   
    due_date = input("Enter due date (YYYY-MM-DD): ")
    while not validate_date(due_date):
        print("Invalid date! Please enter a valid date in YYYY-MM-DD format.")
        due_date = input("Enter due date (YYYY-MM-DD): ")
    
    task = {
        "name": task_name,
        "description": task_description,
        "priority": task_priority.capitalize(),
        "due_date": due_date
    }
    
    tasks.append(task)
    print(f"Task '{task_name}' added successfully!")
    
#Function to view all tasks
def view_tasks():
    # Check if tasks are available
    if not tasks:
        print("No tasks available.")
    else:
        # Display details of each task
        for index in range(len(tasks)):
            task = tasks[index]
            print(f"\nTask {index + 1}:")
            print(f"  Name        : {task['name']}")
            print(f"  Description : {task['description']}")
            print(f"  Priority    : {task['priority'].capitalize()}")
            print(f"  Due Date    : {task['due_date']}")
   
#Function to update a task
def update_task():
    view_tasks()
    if not tasks:
        
        return
        
    try:
        task_index = int(input("Enter the task number to update: ")) - 1
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            print(f"Updating Task: {task['name']}")
            
            new_name = input(f"Enter new task name (leave blank to keep current: {task['name']}): ") or task['name']
            new_description = input(f"Enter new description (leave blank to keep current: {task['description']}): ") or task['description']
            
            new_priority = input(f"Enter new priority (High/Medium/Low, leave blank to keep current: {task['priority']}): ") or task['priority']
            while new_priority != task['priority'] and not validate_priority(new_priority):
                new_priority = input("Invalid priority. Enter priority (High/Medium/Low): ")
            
            
            new_due_date = input(f"Enter new due date (YYYY-MM-DD, leave blank to keep current: {task['due_date']}): ") or task['due_date']
            while new_due_date != task['due_date'] and not validate_date(new_due_date):
                
                new_due_date = input(f"Enter new due date (YYYY-MM-DD): ")
            
            
            task['name'] = new_name
            task['description'] = new_description
            task['priority'] = new_priority.capitalize()
            task['due_date'] = new_due_date
             
            print("Task updated successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

#Function to delete a task
def delete_task():
    view_tasks()
    if not tasks:
        return  # Exit if there are no tasks
    
    while True:
        try:
             # Get task index to delete
            task_index = int(input("Enter the task number to delete (or 0 to cancel): ")) - 1
            if task_index == -1:
                print("Deletion cancelled.")
                break
            elif 0 <= task_index < len(tasks): # Check if the task index is valid
                removed_task = tasks.pop(task_index)
                print(f"Task '{removed_task['name']}' deleted successfully!")
                break
            else:
                print("Invalid task number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

# json File Handling Functions

def load_tasks_from_json():
    global tasks
    try:
        with open(FILE_NAME, "r") as file:
            tasks = json.load(file)
        print(f"Loaded {len(tasks)} task(s) loaded from '{FILE_NAME}'.")
    except FileNotFoundError:
        tasks = []
        with open(FILE_NAME, "w") as file:
            json.dump(tasks, file)
        print("No previous file found. Created a new 'tasks.json'.")

def save_tasks_to_json():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)
    print(f"Tasks saved to file. Total: {len(tasks)}")



# Main function to test CRUD operations
if __name__ == "__main__":
    # Load previously saved tasks if any
    load_tasks_from_json()
    
    while True:
        # Display menu options
        print("\nTask Manager")
        print("1. Add Tasks")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Save and Exit")

        try:
            # Take user input for menu choice
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_task()
                save_tasks_to_json()  # Save after adding
            elif choice == 2:
                view_tasks()
            elif choice == 3:
                update_task()
                save_tasks_to_json()  # Save after updating
            elif choice == 4:
                delete_task()
                save_tasks_to_json()  # Save after deleting
            elif choice == 5:
                print("Exiting Task Manager. Best of luck with your tasks!")
               
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number or task index.")
