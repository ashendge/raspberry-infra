#!/usr/bin/env python3
"""
SRE Interview Prep Roadmap Application
A Flask-based web application for tracking interview preparation progress
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Use persistent database path
DB_PATH = os.environ.get('DB_PATH', '/app/data/roadmap.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

db = SQLAlchemy(app)

# Database Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), default='#3B82F6')
    topics = db.relationship('Topic', backref='category', lazy=True, cascade='all, delete-orphan')

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subtopics = db.relationship('Subtopic', backref='topic', lazy=True, cascade='all, delete-orphan')

class Subtopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Database initialization with better error handling
def init_db():
    """Initialize database with proper error handling and logging"""
    with app.app_context():
        try:
            # Create tables
            db.create_all()
            print(f"Database initialized at: {DB_PATH}")
            
            # Check if data already exists
            if Category.query.first():
                print("Database already contains data, skipping seed.")
                return
            
            print("Seeding database with initial data...")
            seed_database()
            print("Database seeded successfully!")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

def seed_database():
    """Seed database with initial data"""
    # Create expanded categories
    categories = [
        Category(name='Coding', color='#8B5CF6'),
        Category(name='System Design / Infra', color='#3B82F6'),
        Category(name='SRE / Reliability', color='#10B981'),
        Category(name='Leadership / Soft Skills', color='#F59E0B'),
        Category(name='OS Fundamentals', color='#EF4444'),
        Category(name='Networking Fundamentals', color='#06B6D4'),
        Category(name='OS + Networking Advanced', color='#8B5CF6'),
        Category(name='Linux Boot Process', color='#F97316'),
        Category(name='Practice Ramp-up + Mock Prep', color='#84CC16'),
        Category(name='Intermediate: SRE Tooling + Deeper Coding', color='#A855F7'),
        Category(name='Infra: Hands-on Tools + Practical Design', color='#0EA5E9'),
        Category(name='Real-world Architecture + Retrospectives', color='#F59E0B'),
        Category(name='Advanced Scaling and Cloud Architecture', color='#10B981'),
        Category(name='Mock Prep + Deep Dive', color='#DC2626'),
        Category(name='Interview Season: Company-specific Focus', color='#7C3AED')
    ]
    
    for cat in categories:
        db.session.add(cat)
    db.session.commit()
    
    # Enhanced data with new categories
    sample_data = [
        # June 2025 - Foundation Building
        {'category': 'Coding', 'month': 'June 2025', 'title': 'Leetcode 150 (easy-medium)', 
         'subtopics': ['Easy Problems (50)', 'Medium Problems (50)', 'Arrays & Hashing Review', 'Two Pointers Practice']},
        {'category': 'System Design / Infra', 'month': 'June 2025', 'title': 'System design basics', 
         'subtopics': ['CAP Theorem', 'Load Balancing Concepts', 'Basic Architecture Patterns', 'Scalability Fundamentals']},
        {'category': 'SRE / Reliability', 'month': 'June 2025', 'title': 'Intro to SRE', 
         'subtopics': ['Incident Lifecycle', 'SRE Principles', 'Reliability Concepts', 'Error Budgets']},
        {'category': 'Leadership / Soft Skills', 'month': 'June 2025', 'title': 'Amazon Leadership Principles', 
         'subtopics': ['STAR Stories Development', 'Behavioral Interview Prep', 'Leadership Scenarios', 'Customer Obsession Examples']},
        {'category': 'OS Fundamentals', 'month': 'June 2025', 'title': 'Process Management Basics', 
         'subtopics': ['Process States', 'Process Scheduling', 'Inter-Process Communication', 'Memory Management Intro']},
        {'category': 'Networking Fundamentals', 'month': 'June 2025', 'title': 'Network Layers & Protocols', 
         'subtopics': ['OSI Model', 'TCP/IP Stack', 'HTTP/HTTPS Basics', 'DNS Fundamentals']},
        
        # July 2025 - Building Core Skills
        {'category': 'Coding', 'month': 'July 2025', 'title': 'Arrays, Two Pointers', 
         'subtopics': ['Array Fundamentals', 'Two Pointer Technique', 'Sliding Window Intro', 'Practice Problems']},
        {'category': 'System Design / Infra', 'month': 'July 2025', 'title': 'App layer: caching, databases', 
         'subtopics': ['Caching Strategies', 'Database Fundamentals', 'SQL vs NoSQL', 'Application Architecture']},
        {'category': 'SRE / Reliability', 'month': 'July 2025', 'title': 'OS: process/thread, Networking: layers, HTTP', 
         'subtopics': ['Process/Thread Management', 'Network Layers (OSI)', 'HTTP Protocol', 'TCP/UDP Differences']},
        {'category': 'Leadership / Soft Skills', 'month': 'July 2025', 'title': 'Project walkthroughs, clear communication', 
         'subtopics': ['Technical Presentation Skills', 'Project Documentation', 'Stakeholder Communication', 'Meeting Facilitation']},
        {'category': 'OS Fundamentals', 'month': 'July 2025', 'title': 'File Systems & I/O', 
         'subtopics': ['File System Types', 'I/O Operations', 'Disk Management', 'File Permissions']},
        {'category': 'Networking Fundamentals', 'month': 'July 2025', 'title': 'Routing & Switching', 
         'subtopics': ['IP Routing', 'Network Switching', 'Subnetting', 'VLAN Concepts']},
        
        # August 2025 - Advanced Concepts
        {'category': 'Coding', 'month': 'August 2025', 'title': 'Sliding Window, Recursion', 
         'subtopics': ['Sliding Window Problems', 'Recursion Patterns', 'Dynamic Programming Intro', 'Backtracking Basics']},
        {'category': 'System Design / Infra', 'month': 'August 2025', 'title': 'DB sharding, replication, queues', 
         'subtopics': ['Database Sharding', 'Master-Slave Replication', 'Message Queues', 'Event-Driven Architecture']},
        {'category': 'SRE / Reliability', 'month': 'August 2025', 'title': 'Debugging distributed systems', 
         'subtopics': ['Distributed System Debugging', 'Observability Tools', 'Tracing & Logging', 'Performance Analysis']},
        {'category': 'Leadership / Soft Skills', 'month': 'August 2025', 'title': 'Behavioral prep kickoff', 
         'subtopics': ['Common Behavioral Questions', 'Failure Stories', 'Conflict Resolution', 'Team Leadership Examples']},
        {'category': 'OS + Networking Advanced', 'month': 'August 2025', 'title': 'Advanced OS & Network Integration', 
         'subtopics': ['Network Stack Implementation', 'Socket Programming', 'System Call Optimization', 'Kernel Networking']},
        {'category': 'Linux Boot Process', 'month': 'August 2025', 'title': 'Boot Sequence Deep Dive', 
         'subtopics': ['GRUB Configuration', 'Kernel Loading', 'Init Systems', 'Service Management']},
        
        # September 2025 - Practice Intensification
        {'category': 'Coding', 'month': 'September 2025', 'title': 'Medium/Hard Leetcode problems', 
         'subtopics': ['Binary Trees Advanced', 'Graph Algorithms', 'Dynamic Programming', 'System Design Coding']},
        {'category': 'System Design / Infra', 'month': 'September 2025', 'title': 'Design: URL shortener, high-traffic APIs', 
         'subtopics': ['URL Shortener Design', 'High-Traffic API Design', 'Rate Limiting', 'CDN Implementation']},
        {'category': 'SRE / Reliability', 'month': 'September 2025', 'title': 'Terraform, CI/CD, monitoring setup', 
         'subtopics': ['Terraform Basics', 'CI/CD Pipelines', 'Monitoring Setup', 'Alerting Systems']},
        {'category': 'Leadership / Soft Skills', 'month': 'September 2025', 'title': 'Cross-functional work, handling failures', 
         'subtopics': ['Cross-Team Collaboration', 'Failure Analysis', 'Post-Mortem Process', 'Incident Communication']},
        {'category': 'Practice Ramp-up + Mock Prep', 'month': 'September 2025', 'title': 'Mock Interview Foundation', 
         'subtopics': ['Mock Interview Setup', 'Interview Formats', 'Time Management', 'Feedback Integration']},
        
        # October 2025 - Intermediate Skills
        {'category': 'Coding', 'month': 'October 2025', 'title': 'Time-boxed practice (45 min)', 
         'subtopics': ['Timed Problem Solving', 'Interview Simulation', 'Code Optimization', 'Edge Case Handling']},
        {'category': 'System Design / Infra', 'month': 'October 2025', 'title': 'Docker, Kubernetes, AWS basics (EC2, S3)', 
         'subtopics': ['Docker Containerization', 'Kubernetes Orchestration', 'AWS EC2 Management', 'S3 Storage Patterns']},
        {'category': 'SRE / Reliability', 'month': 'October 2025', 'title': 'Latency analysis, root cause exercises', 
         'subtopics': ['Latency Analysis', 'Root Cause Analysis', 'Performance Bottlenecks', 'System Optimization']},
        {'category': 'Leadership / Soft Skills', 'month': 'October 2025', 'title': 'Leading real-world projects', 
         'subtopics': ['Project Management', 'Technical Leadership', 'Resource Planning', 'Risk Management']},
        {'category': 'Intermediate: SRE Tooling + Deeper Coding', 'month': 'October 2025', 'title': 'Advanced SRE Tools', 
         'subtopics': ['Prometheus & Grafana', 'ELK Stack', 'Advanced Scripting', 'Automation Frameworks']},
        
        # November 2025 - Hands-on Experience
        {'category': 'Coding', 'month': 'November 2025', 'title': 'Mix of Leetcode + review cycles', 
         'subtopics': ['Algorithm Review', 'Data Structure Mastery', 'Problem Pattern Recognition', 'Speed Optimization']},
        {'category': 'System Design / Infra', 'month': 'November 2025', 'title': 'Feed design, async workflows, event queues', 
         'subtopics': ['Social Media Feed Design', 'Async Processing', 'Event Queue Systems', 'Real-time Updates']},
        {'category': 'SRE / Reliability', 'month': 'November 2025', 'title': 'Incident reviews, playbook design', 
         'subtopics': ['Incident Review Process', 'Playbook Creation', 'Runbook Development', 'Response Automation']},
        {'category': 'Leadership / Soft Skills', 'month': 'November 2025', 'title': 'Ambiguity, stakeholder alignment', 
         'subtopics': ['Handling Ambiguity', 'Stakeholder Management', 'Requirements Gathering', 'Decision Making']},
        {'category': 'Infra: Hands-on Tools + Practical Design', 'month': 'November 2025', 'title': 'Infrastructure Mastery', 
         'subtopics': ['Terraform Advanced', 'Ansible Automation', 'Cloud Architecture', 'Infrastructure as Code']},
        
        # December 2025 - Real-world Application
        {'category': 'Coding', 'month': 'December 2025', 'title': 'Whiteboard practice', 
         'subtopics': ['Whiteboard Coding', 'Communication While Coding', 'Problem Decomposition', 'Iterative Solutions']},
        {'category': 'System Design / Infra', 'month': 'December 2025', 'title': 'Serverless, autoscaling, observability tools', 
         'subtopics': ['Serverless Architecture', 'Auto-scaling Strategies', 'Observability Tools', 'Monitoring Dashboards']},
        {'category': 'SRE / Reliability', 'month': 'December 2025', 'title': 'Outage simulations, failover readiness', 
         'subtopics': ['Chaos Engineering', 'Failover Testing', 'Disaster Recovery', 'Business Continuity']},
        {'category': 'Leadership / Soft Skills', 'month': 'December 2025', 'title': 'Mock behavioral sessions', 
         'subtopics': ['Mock Interviews', 'Behavioral Practice', 'Story Refinement', 'Confidence Building']},
        {'category': 'Real-world Architecture + Retrospectives', 'month': 'December 2025', 'title': 'Architecture Case Studies', 
         'subtopics': ['Real System Analysis', 'Architecture Reviews', 'Post-Mortem Studies', 'Design Retrospectives']},
        
        # January 2026 - Advanced Preparation
        {'category': 'Coding', 'month': 'January 2026', 'title': 'Daily mocks + focused Leetcode', 
         'subtopics': ['Daily Mock Interviews', 'Company-Specific Problems', 'Advanced Algorithms', 'Optimization Techniques']},
        {'category': 'System Design / Infra', 'month': 'January 2026', 'title': 'Full design interviews (GCP-style), edge-case tuning', 
         'subtopics': ['End-to-End System Design', 'GCP Services', 'Edge Case Analysis', 'Scalability Planning']},
        {'category': 'SRE / Reliability', 'month': 'January 2026', 'title': 'Chaos engineering, scenario-based review', 
         'subtopics': ['Chaos Engineering Practices', 'Scenario Planning', 'Fault Injection', 'Resilience Testing']},
        {'category': 'Leadership / Soft Skills', 'month': 'January 2026', 'title': 'Crisis handling, pressure interviews', 
         'subtopics': ['Crisis Management', 'High-Pressure Situations', 'Decision Under Pressure', 'Leadership in Crisis']},
        {'category': 'Advanced Scaling and Cloud Architecture', 'month': 'January 2026', 'title': 'Enterprise Scale Systems', 
         'subtopics': ['Multi-Region Architecture', 'Global Load Balancing', 'Data Consistency', 'Performance at Scale']},
        
        # February 2026 - Final Preparation
        {'category': 'Coding', 'month': 'February 2026', 'title': 'Company-targeted problem sets', 
         'subtopics': ['Google-Style Problems', 'Amazon Coding Standards', 'Facebook/Meta Patterns', 'Apple System Focus']},
        {'category': 'System Design / Infra', 'month': 'February 2026', 'title': 'Production-ready architecture patterns', 
         'subtopics': ['Production Architecture', 'Enterprise Patterns', 'Microservices Design', 'Cloud-Native Patterns']},
        {'category': 'SRE / Reliability', 'month': 'February 2026', 'title': 'SLAs, SLOs, on-call case studies', 
         'subtopics': ['SLA/SLO Definition', 'On-Call Best Practices', 'Case Study Analysis', 'Service Level Management']},
        {'category': 'Leadership / Soft Skills', 'month': 'February 2026', 'title': 'Confidence building, behavioral mastery', 
         'subtopics': ['Final Interview Prep', 'Confidence Techniques', 'Behavioral Mastery', 'Negotiation Skills']},
        {'category': 'Mock Prep + Deep Dive', 'month': 'February 2026', 'title': 'Intensive Mock Sessions', 
         'subtopics': ['Full-Length Mocks', 'Technical Deep Dives', 'Stress Testing', 'Performance Analysis']},
        {'category': 'Interview Season: Company-specific Focus', 'month': 'February 2026', 'title': 'Company Preparation', 
         'subtopics': ['Google SRE Focus', 'Amazon Principles', 'Meta Culture Fit', 'Startup Environment Prep']},
    ]
    
    for item in sample_data:
        category = Category.query.filter_by(name=item['category']).first()
        if category:  # Only add if category exists
            topic = Topic(
                title=item['title'],
                category_id=category.id,
                month=item['month']
            )
            db.session.add(topic)
            db.session.flush()  # To get the topic ID
            
            for subtopic_title in item['subtopics']:
                subtopic = Subtopic(
                    title=subtopic_title,
                    topic_id=topic.id
                )
                db.session.add(subtopic)
    
    db.session.commit()

# Routes
@app.route('/')
def index():
    categories = Category.query.all()
    topics = Topic.query.all()
    
    # Group topics by month in chronological order
    month_order = [
        'June 2025', 'July 2025', 'August 2025', 'September 2025', 
        'October 2025', 'November 2025', 'December 2025', 
        'January 2026', 'February 2026'
    ]
    
    months = {}
    for month in month_order:
        months[month] = []
    
    for topic in topics:
        if topic.month in months:
            months[topic.month].append(topic)
    
    return render_template('index.html', categories=categories, months=months)

@app.route('/tree')
def tree_view():
    categories = Category.query.all()
    
    # Build tree structure organized by category -> month -> topic -> subtopics
    tree_data = []
    
    for category in categories:
        category_data = {
            'name': category.name,
            'color': category.color,
            'months': {}
        }
        
        # Group topics by month for this category
        for topic in category.topics:
            if topic.month not in category_data['months']:
                category_data['months'][topic.month] = []
            
            topic_data = {
                'id': topic.id,
                'title': topic.title,
                'completed': topic.completed,
                'completion_date': topic.completion_date,
                'subtopics': []
            }
            
            for subtopic in topic.subtopics:
                topic_data['subtopics'].append({
                    'id': subtopic.id,
                    'title': subtopic.title,
                    'completed': subtopic.completed,
                    'completion_date': subtopic.completion_date
                })
            
            category_data['months'][topic.month].append(topic_data)
        
        tree_data.append(category_data)
    
    return render_template('tree.html', tree_data=tree_data)

@app.route('/delete_topic/<int:topic_id>', methods=['POST'])
def delete_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    db.session.delete(topic)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_subtopic/<int:subtopic_id>', methods=['POST'])
def delete_subtopic(subtopic_id):
    subtopic = Subtopic.query.get_or_404(subtopic_id)
    db.session.delete(subtopic)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_topic/<int:topic_id>', methods=['GET', 'POST'])
def edit_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    categories = Category.query.all()
    if request.method == 'POST':
        topic.title = request.form['title']
        topic.description = request.form.get('description', '')
        topic.category_id = request.form['category_id']
        topic.month = request.form['month']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_topic.html', topic=topic, categories=categories)

@app.route('/edit_subtopic/<int:subtopic_id>', methods=['GET', 'POST'])
def edit_subtopic(subtopic_id):
    subtopic = Subtopic.query.get_or_404(subtopic_id)
    if request.method == 'POST':
        subtopic.title = request.form['title']
        subtopic.description = request.form.get('description', '')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_subtopic.html', subtopic=subtopic)

@app.route('/api/topics')
def get_topics():
    topics = Topic.query.all()
    result = []
    for topic in topics:
        subtopics = [{'id': s.id, 'title': s.title, 'completed': s.completed} 
                    for s in topic.subtopics]
        result.append({
            'id': topic.id,
            'title': topic.title,
            'category': topic.category.name,
            'category_color': topic.category.color,
            'month': topic.month,
            'completed': topic.completed,
            'subtopics': subtopics
        })
    return jsonify(result)

@app.route('/api/topics/<int:topic_id>/toggle', methods=['POST'])
def toggle_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    topic.completed = not topic.completed
    topic.completion_date = date.today() if topic.completed else None
    db.session.commit()
    return jsonify({'success': True, 'completed': topic.completed})

@app.route('/api/subtopics/<int:subtopic_id>/toggle', methods=['POST'])
def toggle_subtopic(subtopic_id):
    subtopic = Subtopic.query.get_or_404(subtopic_id)
    subtopic.completed = not subtopic.completed
    subtopic.completion_date = date.today() if subtopic.completed else None
    db.session.commit()
    
    # Check if all subtopics are completed to auto-complete the topic
    topic = subtopic.topic
    all_completed = all(s.completed for s in topic.subtopics)
    if all_completed and not topic.completed:
        topic.completed = True
        topic.completion_date = date.today()
        db.session.commit()
    
    return jsonify({'success': True, 'completed': subtopic.completed})

@app.route('/add_topic', methods=['GET', 'POST'])
def add_topic():
    if request.method == 'POST':
        category_id = request.form['category_id']
        title = request.form['title']
        month = request.form['month']
        description = request.form.get('description', '')
        
        topic = Topic(
            title=title,
            description=description,
            category_id=category_id,
            month=month
        )
        db.session.add(topic)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    categories = Category.query.all()
    return render_template('add_topic.html', categories=categories)

@app.route('/add_subtopic/<int:topic_id>', methods=['GET', 'POST'])
def add_subtopic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        
        subtopic = Subtopic(
            title=title,
            description=description,
            topic_id=topic_id
        )
        db.session.add(subtopic)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_subtopic.html', topic=topic)

@app.route('/progress')
def progress():
    categories = Category.query.all()
    progress_data = []
    
    for category in categories:
        total_topics = len(category.topics)
        completed_topics = len([t for t in category.topics if t.completed])
        
        total_subtopics = sum(len(t.subtopics) for t in category.topics)
        completed_subtopics = sum(len([s for s in t.subtopics if s.completed]) for t in category.topics)
        
        progress_data.append({
            'category': category.name,
            'color': category.color,
            'topics_progress': (completed_topics / total_topics * 100) if total_topics > 0 else 0,
            'subtopics_progress': (completed_subtopics / total_subtopics * 100) if total_subtopics > 0 else 0,
            'completed_topics': completed_topics,
            'total_topics': total_topics,
            'completed_subtopics': completed_subtopics,
            'total_subtopics': total_subtopics
        })
    
    return render_template('progress.html', progress_data=progress_data)

@app.route('/reset_db')
def reset_db():
    """Reset database - useful for development"""
    try:
        db.drop_all()
        seed_database()
        return jsonify({'success': True, 'message': 'Database reset successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error resetting database: {e}'})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        Category.query.first()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'db_path': DB_PATH
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'db_path': DB_PATH
        }), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_ENV') != 'production')