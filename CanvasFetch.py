import requests
import json
import os


# Canvas API Configuration
CANVAS_API_URL = "https://gatech.instructure.com/api/v1"
CANVAS_API_KEY = "2096~ktDPU4hMtR2R34tHc3zQtQ9DDJXRh9azt8yAx7B7NMTTR8KTNTycYenGMkL9Phx3"

canvas_headers = {
    "Authorization": f"Bearer {CANVAS_API_KEY}"
}

def list_courses():
    url = f"{CANVAS_API_URL}/courses"
    params = {"enrollment_state": "active"}  # Fetch courses with all enrollment states
    courses = []

    print("Fetching courses...")
    while url:
        response = requests.get(url, headers=canvas_headers, params=params)
        if response.status_code == 200:
            courses.extend(response.json())
            # Handle pagination by checking the 'next' link in the response
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                url = None
        else:
            print("Error fetching courses:", response.status_code, response.text)
            break

    # Print courses for debugging
    print(f"Total courses fetched: {len(courses)}")
    for course in courses:
        course_id = course.get('id', 'Unknown ID')
        course_name = course.get('name', 'Unnamed Course')
        print(f"Course ID: {course_id}, Name: {course_name}")
    
    return courses

# Fetch details of a specific course by ID (for debugging missing courses)
def get_course(course_id):
    url = f"{CANVAS_API_URL}/courses/{course_id}"
    response = requests.get(url, headers=canvas_headers)
    if response.status_code == 200:
        print("Course details:")
        print(response.json())
    else:
        print(f"Error fetching course {course_id}: {response.status_code}, {response.text}")

# Fetch assignments for a specific course
def fetch_assignments(course_id):
    url = f"{CANVAS_API_URL}/courses/{course_id}/assignments"
    response = requests.get(url, headers=canvas_headers)
    if response.status_code == 200:
        assignments = response.json()
        print(f"Assignments for course {course_id}:")
        for assignment in assignments:
            assignment_name = assignment.get('name', 'Unnamed Assignment')
            due_date = assignment.get('due_at', 'No due date')
            print(f"  - {assignment_name}, Due: {due_date}")
        return assignments
    else:
        print(f"Error fetching assignments for course {course_id}: {response.status_code}, {response.text}")
        return []

# Append assignments to a JSON file
def append_to_json(assignments, course_name, output_file="all_assignments.json"):
    # Load existing data if file exists
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Add assignments with course name
    for assignment in assignments:
        data.append({
            "course_name": course_name,
            "assignment_name": assignment.get("name", "Unnamed Assignment"),
            "due_at": assignment.get("due_at", None),
            "id": assignment.get("id", None)
        })

    # Save back to JSON file
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Appended {len(assignments)} assignments from {course_name} to {output_file}")

# Main function
if __name__ == "__main__":
    courses = [(423818, "Computer Organiz&Program - CS-2110-A/B/C/D/E/GR")
               ,(436466, "Idea 2 Prototype")
               ,(422930, "Intro-Artificial Intell - CS-3600-A/B/C/D")
               ,(438624, "Objects and Design - CS-2340-C")
               ,(448358, "Special Topics - CX-4803-GPU")
               ,(427862, "Spring 25 ML 4641")
               ,(450486, "VIP Proj Team: JR I - VIP-3601-VYR")]
    
    for course_id, course_name in courses:
        assignments = fetch_assignments(course_id)
        append_to_json(assignments, course_name)