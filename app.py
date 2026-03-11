from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'replace-with-a-secret-key' # Use a strong, random key in production

# Simple in-memory user store (replace with a database like Firebase/Firestore/SQL in a real app)
users = {}

branches = [
    "Computer Science & Engineering", "Electronics & Communication Engineering",
    "Electrical & Electronics Engineering", "Mechanical Engineering", "Civil Engineering",
    "Chemical Engineering", "Aerospace Engineering", "Biotechnology Engineering",
    "Artificial Intelligence & Machine Learning", "Data Science"
]
interests = [
    "Technology & Programming", "Design & Creativity", "Business & Entrepreneurship",
    "Health & Medicine", "Science & Research", "Arts & Literature",
    "Social Sciences", "Law & Politics"
]

# Each course now has both branch and interest for filtering!
# Expanded course list to cover a wider range of combinations.
courses = [
    # --- Original Courses (Kept for continuity) ---
    {
        "title": "Data Structures and Algorithms",
        "branch": "Computer Science & Engineering",
        "interest": "Technology & Programming",
        "category": "Technology & Programming",
        "platform": "Coursera",
        "duration": "8 weeks",
        "level": "Beginner",
        "rating": 4.7,
        "students": 3500,
        "description": "Learn core data structures and algorithms in Python.",
        "link": "https://www.coursera.org/learn/data-structures-algorithms"
    },
    {
        "title": "Introduction to Robotics",
        "branch": "Mechanical Engineering",
        "interest": "Technology & Programming",
        "category": "Engineering",
        "platform": "edX",
        "duration": "10 weeks",
        "level": "Intermediate",
        "rating": 4.6,
        "students": 1900,
        "description": "The basics of robotic system design, actuation, and control.",
        "link": "https://www.edx.org/course/introduction-to-robotics"
    },
    {
        "title": "Electronic Circuit Design",
        "branch": "Electrical & Electronics Engineering",
        "interest": "Science & Research",
        "category": "Engineering",
        "platform": "Udemy",
        "duration": "7 weeks",
        "level": "Beginner",
        "rating": 4.5,
        "students": 2100,
        "description": "Hands-on learning for designing and analyzing electronic circuits.",
        "link": "https://www.udemy.com/course/electronic-circuit-design"
    },
    {
        "title": "Urban Planning & Design",
        "branch": "Civil Engineering",
        "interest": "Design & Creativity",
        "category": "Civil Engineering",
        "platform": "FutureLearn",
        "duration": "6 weeks",
        "level": "Beginner",
        "rating": 4.8,
        "students": 1200,
        "description": "Basics of designing sustainable urban environments.",
        "link": "https://www.futurelearn.com/courses/urban-planning"
    },
    {
        "title": "Fundamentals of Biochemistry",
        "branch": "Biotechnology Engineering",
        "interest": "Health & Medicine",
        "category": "Biochemistry",
        "platform": "Coursera",
        "duration": "9 weeks",
        "level": "Beginner",
        "rating": 4.9,
        "students": 1800,
        "description": "Core principles of biochemistry and applications in health.",
        "link": "https://www.coursera.org/learn/biochemistry"
    },
    {
        "title": "Machine Learning with Python",
        "branch": "Data Science",
        "interest": "Technology & Programming",
        "category": "Data Science",
        "platform": "Coursera",
        "duration": "12 weeks",
        "level": "Intermediate",
        "rating": 4.8,
        "students": 2100,
        "description": "Build intelligent applications using Python and scikit-learn.",
        "link": "https://www.coursera.org/learn/machine-learning-with-python"
    },
    {
        "title": "Aerospace Propulsion",
        "branch": "Aerospace Engineering",
        "interest": "Science & Research",
        "category": "Engineering",
        "platform": "edX",
        "duration": "8 weeks",
        "level": "Advanced",
        "rating": 4.6,
        "students": 1200,
        "description": "Propulsion principles and their applications in aircraft and rockets.",
        "link": "https://www.edx.org/course/aerospace-propulsion"
    },

    # --- New Courses Added for better coverage ---

    # Computer Science & Engineering
    {
        "title": "Full-Stack Web Development (React/Node)",
        "branch": "Computer Science & Engineering",
        "interest": "Design & Creativity",
        "category": "Development",
        "platform": "Udemy",
        "duration": "16 weeks",
        "level": "Intermediate",
        "rating": 4.5,
        "students": 5100,
        "description": "Master modern full-stack development with JavaScript frameworks.",
        "link": "https://www.udemy.com/course/full-stack-web-dev"
    },
    {
        "title": "Blockchain Development and Finance",
        "branch": "Computer Science & Engineering",
        "interest": "Business & Entrepreneurship",
        "category": "FinTech",
        "platform": "edX",
        "duration": "10 weeks",
        "level": "Advanced",
        "rating": 4.4,
        "students": 900,
        "description": "Build decentralized applications and understand crypto-economics.",
        "link": "https://www.edx.org/course/blockchain-finance"
    },

    # Electronics & Communication Engineering
    {
        "title": "Embedded Systems Programming",
        "branch": "Electronics & Communication Engineering",
        "interest": "Technology & Programming",
        "category": "Hardware/Software",
        "platform": "Coursera",
        "duration": "7 weeks",
        "level": "Intermediate",
        "rating": 4.7,
        "students": 2500,
        "description": "Programming microcontrollers for IoT and real-time systems.",
        "link": "https://www.coursera.org/learn/embedded-systems"
    },
    {
        "title": "Patent Law for Engineers",
        "branch": "Electronics & Communication Engineering",
        "interest": "Law & Politics",
        "category": "Legal",
        "platform": "FutureLearn",
        "duration": "4 weeks",
        "level": "Beginner",
        "rating": 4.3,
        "students": 800,
        "description": "Understanding intellectual property and patent filing in tech.",
        "link": "https://www.futurelearn.com/courses/patent-law-for-engineers"
    },

    # Electrical & Electronics Engineering
    {
        "title": "Renewable Energy Systems and Grid Integration",
        "branch": "Electrical & Electronics Engineering",
        "interest": "Science & Research",
        "category": "Energy",
        "platform": "MIT OpenCourseWare",
        "duration": "14 weeks",
        "level": "Advanced",
        "rating": 4.8,
        "students": 1500,
        "description": "Deep dive into solar, wind, and smart grid technologies.",
        "link": "https://ocw.mit.edu/courses/renewable-energy"
    },
    {
        "title": "Power Electronics and IoT",
        "branch": "Electrical & Electronics Engineering",
        "interest": "Technology & Programming",
        "category": "Power Systems",
        "platform": "edX",
        "duration": "9 weeks",
        "level": "Intermediate",
        "rating": 4.5,
        "students": 1100,
        "description": "Designing efficient power conversion systems for connected devices.",
        "link": "https://www.edx.org/course/power-electronics-iot"
    },

    # Mechanical Engineering
    {
        "title": "Solid Modeling using CAD",
        "branch": "Mechanical Engineering",
        "interest": "Design & Creativity",
        "category": "Design",
        "platform": "Coursera",
        "duration": "6 weeks",
        "level": "Beginner",
        "rating": 4.6,
        "students": 3200,
        "description": "Learn 3D modeling and assembly design using professional CAD software.",
        "link": "https://www.coursera.org/learn/solid-modeling"
    },
    {
        "title": "Introduction to Biomechanics",
        "branch": "Mechanical Engineering",
        "interest": "Health & Medicine",
        "category": "Biomedical",
        "platform": "Udemy",
        "duration": "8 weeks",
        "level": "Intermediate",
        "rating": 4.7,
        "students": 1400,
        "description": "Analyze the mechanics of human movement and biological systems.",
        "link": "https://www.udemy.com/course/introduction-to-biomechanics"
    },

    # Civil Engineering
    {
        "title": "Construction Project Management",
        "branch": "Civil Engineering",
        "interest": "Business & Entrepreneurship",
        "category": "Management",
        "platform": "edX",
        "duration": "12 weeks",
        "level": "Intermediate",
        "rating": 4.5,
        "students": 1800,
        "description": "Principles and tools for effective construction project execution.",
        "link": "https://www.edx.org/course/construction-project-management"
    },
    {
        "title": "Sustainable Urban Development",
        "branch": "Civil Engineering",
        "interest": "Social Sciences",
        "category": "Policy",
        "platform": "Coursera",
        "duration": "10 weeks",
        "level": "Advanced",
        "rating": 4.7,
        "students": 950,
        "description": "Examines policy and social impacts of sustainable infrastructure.",
        "link": "https://www.coursera.org/learn/sustainable-urban-development"
    },

    # Chemical Engineering
    {
        "title": "Catalysis and Reaction Engineering",
        "branch": "Chemical Engineering",
        "interest": "Science & Research",
        "category": "Core Chem",
        "platform": "edX",
        "duration": "8 weeks",
        "level": "Advanced",
        "rating": 4.6,
        "students": 1050,
        "description": "In-depth study of catalytic processes and reactor design.",
        "link": "https://www.edx.org/course/catalysis-reaction-engineering"
    },
    {
        "title": "Drug Delivery Systems",
        "branch": "Chemical Engineering",
        "interest": "Health & Medicine",
        "category": "Pharmaceutical",
        "platform": "Coursera",
        "duration": "7 weeks",
        "level": "Intermediate",
        "rating": 4.8,
        "students": 1300,
        "description": "Formulation and optimization of controlled drug release systems.",
        "link": "https://www.coursera.org/learn/drug-delivery-systems"
    },

    # Aerospace Engineering
    {
        "title": "Aircraft Interior Design & Ergonomics",
        "branch": "Aerospace Engineering",
        "interest": "Design & Creativity",
        "category": "Design",
        "platform": "Udemy",
        "duration": "6 weeks",
        "level": "Beginner",
        "rating": 4.4,
        "students": 850,
        "description": "Focuses on cabin layout, materials, and passenger comfort.",
        "link": "https://www.udemy.com/course/aircraft-interior-design"
    },
    {
        "title": "Flight Simulation Programming",
        "branch": "Aerospace Engineering",
        "interest": "Technology & Programming",
        "category": "Software",
        "platform": "edX",
        "duration": "10 weeks",
        "level": "Intermediate",
        "rating": 4.7,
        "students": 1100,
        "description": "Develop flight models and visualization tools using C++ or Python.",
        "link": "https://www.edx.org/course/flight-simulation-programming"
    },

    # Biotechnology Engineering
    {
        "title": "Regulatory Affairs in Biotechnology",
        "branch": "Biotechnology Engineering",
        "interest": "Business & Entrepreneurship",
        "category": "Compliance",
        "platform": "FutureLearn",
        "duration": "5 weeks",
        "level": "Intermediate",
        "rating": 4.5,
        "students": 700,
        "description": "Navigating FDA and global regulations for biotech products.",
        "link": "https://www.futurelearn.com/courses/biotech-regulatory-affairs"
    },
    {
        "title": "Genetic Engineering Techniques",
        "branch": "Biotechnology Engineering",
        "interest": "Science & Research",
        "category": "Lab Skills",
        "platform": "Coursera",
        "duration": "11 weeks",
        "level": "Advanced",
        "rating": 4.9,
        "students": 1600,
        "description": "Practical methods in gene editing (CRISPR), cloning, and sequencing.",
        "link": "https://www.coursera.org/learn/genetic-engineering"
    },

    # Artificial Intelligence & Machine Learning
    {
        "title": "Deep Learning Specialization",
        "branch": "Artificial Intelligence & Machine Learning",
        "interest": "Technology & Programming",
        "category": "Advanced ML",
        "platform": "Coursera",
        "duration": "20 weeks",
        "level": "Advanced",
        "rating": 4.9,
        "students": 4000,
        "description": "Five-course specialization on neural networks and deep learning.",
        "link": "https://www.coursera.org/specializations/deep-learning"
    },
    {
        "title": "Generative AI for Content Creation",
        "branch": "Artificial Intelligence & Machine Learning",
        "interest": "Arts & Literature",
        "category": "Creative AI",
        "platform": "edX",
        "duration": "6 weeks",
        "level": "Beginner",
        "rating": 4.5,
        "students": 1500,
        "description": "Use generative models to create text, images, and music.",
        "link": "https://www.edx.org/course/generative-ai-content"
    },
    {
        "title": "Ethics and Governance of AI",
        "branch": "Artificial Intelligence & Machine Learning",
        "interest": "Law & Politics",
        "category": "Policy",
        "platform": "FutureLearn",
        "duration": "8 weeks",
        "level": "Intermediate",
        "rating": 4.6,
        "students": 900,
        "description": "Legal and ethical challenges in deploying intelligent systems.",
        "link": "https://www.futurelearn.com/courses/ethics-of-ai"
    },

    # Data Science
    {
        "title": "Data Storytelling for Executives",
        "branch": "Data Science",
        "interest": "Business & Entrepreneurship",
        "category": "Communication",
        "platform": "Udemy",
        "duration": "4 weeks",
        "level": "Intermediate",
        "rating": 4.4,
        "students": 1000,
        "description": "Communicate complex data findings clearly to decision-makers.",
        "link": "https://www.udemy.com/course/data-storytelling"
    },
    {
        "title": "Interactive Data Visualization (D3.js)",
        "branch": "Data Science",
        "interest": "Design & Creativity",
        "category": "Visualization",
        "platform": "edX",
        "duration": "9 weeks",
        "level": "Advanced",
        "rating": 4.7,
        "students": 1400,
        "description": "Building custom, interactive visualizations for the web.",
        "link": "https://www.edx.org/course/data-visualization-d3js"
    },
    {
        "title": "Statistical Methods for Data Mining",
        "branch": "Data Science",
        "interest": "Science & Research",
        "category": "Statistics",
        "platform": "Coursera",
        "duration": "10 weeks",
        "level": "Advanced",
        "rating": 4.8,
        "students": 1200,
        "description": "Rigorous statistical foundations for large-scale data analysis.",
        "link": "https://www.coursera.org/learn/statistical-methods-data-mining"
    },

    # Arts & Literature / Social Sciences focused additions
    {
        "title": "History of Technology and Society",
        "branch": "Computer Science & Engineering",
        "interest": "Social Sciences",
        "category": "Humanities",
        "platform": "edX",
        "duration": "8 weeks",
        "level": "Beginner",
        "rating": 4.2,
        "students": 600,
        "description": "Examines the impact of computing on culture and politics.",
        "link": "https://www.edx.org/course/history-of-technology"
    },
    {
        "title": "Creative Writing for Engineers",
        "branch": "Mechanical Engineering",
        "interest": "Arts & Literature",
        "category": "Communication",
        "platform": "FutureLearn",
        "duration": "4 weeks",
        "level": "Beginner",
        "rating": 4.5,
        "students": 500,
        "description": "Develop technical communication and creative storytelling skills.",
        "link": "https://www.futurelearn.com/courses/creative-writing-for-engineers"
    },
]

@app.route('/')
def home():
    # Placeholder: Assuming you have a landing.html template
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Placeholder: Assuming you have a login.html template
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials. Please try again.', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Placeholder: Assuming you have a signup.html template
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists.', 'warning')
        else:
            users[username] = password
            flash('Signup success! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Placeholder: Assuming you have a dashboard.html template
    if 'user' not in session:
        flash('You must be logged in to access the dashboard.', 'error')
        return redirect(url_for('login'))

    selected_courses = []
    selected_branch = ''
    selected_interest = ''

    if request.method == 'POST':
        selected_branch = request.form.get('branch')
        selected_interest = request.form.get('interest')
        
        # Filtering logic remains the same: courses must match BOTH branch and interest
        selected_courses = [
            c for c in courses 
            if c["branch"] == selected_branch and c["interest"] == selected_interest
        ]
        
        if not selected_courses:
             flash(f'No courses found for {selected_branch} interested in {selected_interest}. Try another combination!', 'info')
        else:
             flash(f'Showing {len(selected_courses)} course(s) for your selection.', 'success')
             
    # If it's a GET request, just show the filters and no courses initially
    elif request.method == 'GET':
        # Optional: Show a few default courses or an empty list
        pass
        
    return render_template('dashboard.html',
        username=session['user'],
        branches=branches,
        interests=interests,
        branch=selected_branch,
        interest=selected_interest,
        courses=selected_courses)
if __name__ == "__main__":
    app.run(debug=True)
