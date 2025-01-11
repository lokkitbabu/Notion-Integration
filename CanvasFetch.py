import requests

CANVAS_API_URL = "https://gatech.instructure.com/api/v1"
API_KEY = "2096~ktDPU4hMtR2R34tHc3zQtQ9DDJXRh9azt8yAx7B7NMTTR8KTNTycYenGMkL9Phx3"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def list_courses():
    url = f"{CANVAS_API_URL}/courses"
    params = {"enrollment_state": "all"}  # Fetch courses with all enrollment states
    courses = []

    print("Fetching courses...")
    while url:
        response = requests.get(url, headers=headers, params=params)
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
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Course details:")
        print(response.json())
    else:
        print(f"Error fetching course {course_id}: {response.status_code}, {response.text}")

# Fetch assignments for a specific course
def fetch_assignments(course_id):
    url = f"{CANVAS_API_URL}/courses/{course_id}/assignments"
    response = requests.get(url, headers=headers)
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

# Main function to test the script
if __name__ == "__main__":
    # List all courses
    courses = list_courses()
    #fetch_assignments(438624)
    get_course(405654)
