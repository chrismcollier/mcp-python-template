import os
import json
import uuid
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import anthropic
from docx import Document
from datetime import datetime
import shutil

from outlines import GENRE_PLOTS

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Configuration
UPLOAD_FOLDER = 'uploads'
BOOKS_FOLDER = 'generated_books'
TEMPLATE_FILE = 'template.docx'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BOOKS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Genre and plot data
# GENRE_PLOTS = {
#     "Sci-fi": [
#         {
#             "title": "Space Adventure",
#             "outline": """
#             Chapter 1: {child_name} discovers a mysterious device in their backyard that transports them to a space station
#             Chapter 2: Meeting alien friends who need help saving their planet from asteroid collision
#             Chapter 3: Learning to pilot a spaceship and understanding alien technology
#             Chapter 4: The dangerous journey through the asteroid field
#             Chapter 5: Discovering the power of teamwork and friendship across species
#             Chapter 6: Using {child_interests} skills to solve the crisis
#             Chapter 7: The final mission to redirect the asteroids
#             Chapter 8: Celebration and saying goodbye to alien friends
#             Chapter 9: Returning home with new perspective on the universe
#             Chapter 10: Sharing the adventure and inspiring others to look to the stars
#             """
#         },
#         {
#             "title": "Time Travel Quest",
#             "outline": """
#             Chapter 1: {child_name} finds an ancient watch that can travel through time
#             Chapter 2: First trip to the dinosaur era - learning about prehistoric life
#             Chapter 3: Accidentally changing something in the past and seeing consequences
#             Chapter 4: Traveling to the future to understand what went wrong
#             Chapter 5: Meeting future versions of themselves and getting advice
#             Chapter 6: Using {child_interests} knowledge to fix the timeline
#             Chapter 7: Racing against time to undo the changes
#             Chapter 8: Learning the responsibility that comes with power
#             Chapter 9: Returning to the present with valuable lessons
#             Chapter 10: Deciding to use the watch wisely to help others
#             """
#         }
#     ],
#     "Fantasy": [
#         {
#             "title": "Magical Kingdom",
#             "outline": """
#             Chapter 1: {child_name} discovers they have magical powers on their {child_age}th birthday
#             Chapter 2: A magical creature guides them to a hidden kingdom in danger
#             Chapter 3: Meeting other young wizards and learning about their unique abilities
#             Chapter 4: The dark sorcerer threatens to steal all magic from the kingdom
#             Chapter 5: Training with wise mentors to strengthen magical skills
#             Chapter 6: Using {child_interests} passion to create a powerful spell
#             Chapter 7: The great battle against the dark forces
#             Chapter 8: Discovering that friendship is the strongest magic
#             Chapter 9: Restoring peace to the magical kingdom
#             Chapter 10: Becoming a guardian of magic in both worlds
#             """
#         },
#         {
#             "title": "Dragon's Secret",
#             "outline": """
#             Chapter 1: {child_name} finds an injured baby dragon hidden in the forest
#             Chapter 2: Learning to care for and communicate with the dragon
#             Chapter 3: Discovering that dragons are misunderstood, not dangerous
#             Chapter 4: The dragon's family is in trouble - captured by dragon hunters
#             Chapter 5: Planning a rescue mission using {child_traits} cleverness
#             Chapter 6: Infiltrating the hunter's camp with dragon friend
#             Chapter 7: The daring escape and reunion with dragon family
#             Chapter 8: Convincing the village that dragons are friends, not foes
#             Chapter 9: Establishing peace between humans and dragons
#             Chapter 10: Becoming the first Dragon Ambassador
#             """
#         }
#     ],
#     "Mystery": [
#         {
#             "title": "School Detective",
#             "outline": """
#             Chapter 1: Strange things keep disappearing at {child_name}'s school
#             Chapter 2: Forming a detective club with friends to solve the mystery
#             Chapter 3: Gathering clues and interviewing witnesses
#             Chapter 4: Following false leads and learning from mistakes
#             Chapter 5: Discovering a pattern in the thefts using {child_interests} skills
#             Chapter 6: The trail leads to an unexpected suspect
#             Chapter 7: Setting a trap to catch the real culprit
#             Chapter 8: The surprising truth behind the mysterious disappearances
#             Chapter 9: Solving the case and helping the real reason behind the thefts
#             Chapter 10: Being recognized as the school's hero detective
#             """
#         },
#         {
#             "title": "Neighborhood Secrets",
#             "outline": """
#             Chapter 1: {child_name} notices their elderly neighbor acting suspiciously
#             Chapter 2: Deciding to investigate despite friends thinking they're imagining things
#             Chapter 3: Discovering secret meetings and mysterious packages
#             Chapter 4: Following clues that lead to more questions than answers
#             Chapter 5: Using {child_traits} persistence to piece together the puzzle
#             Chapter 6: Uncovering a network of neighbors with a wonderful secret
#             Chapter 7: Learning they're organizing a surprise community garden
#             Chapter 8: Realizing assumptions can be wrong and people can surprise you
#             Chapter 9: Joining the secret project and contributing {child_interests} expertise
#             Chapter 10: The grand reveal that brings the whole neighborhood together
#             """
#         }
#     ],
#     "Adventure": [
#         {
#             "title": "Treasure Hunt",
#             "outline": """
#             Chapter 1: {child_name} discovers an old treasure map in their attic
#             Chapter 2: Convincing friends to join the treasure hunting expedition
#             Chapter 3: Following the first clues leads to the local park
#             Chapter 4: Overcoming obstacles and solving riddles along the way
#             Chapter 5: Using {child_interests} knowledge to decode ancient symbols
#             Chapter 6: The trail leads to dangerous but exciting locations
#             Chapter 7: Working as a team to overcome the final challenges
#             Chapter 8: Finding the treasure isn't gold, but something more valuable
#             Chapter 9: Discovering the real treasure was the adventure and friendships
#             Chapter 10: Deciding to create their own treasure hunt for others
#             """
#         },
#         {
#             "title": "Wilderness Survival",
#             "outline": """
#             Chapter 1: {child_name}'s family camping trip takes an unexpected turn
#             Chapter 2: Getting separated from parents during a storm
#             Chapter 3: Using survival skills and staying calm in scary situations  
#             Chapter 4: Meeting forest animals who become helpful companions
#             Chapter 5: Learning to find food, water, and shelter using {child_traits}
#             Chapter 6: Facing biggest fears and discovering inner strength
#             Chapter 7: The journey to find the way back to civilization
#             Chapter 8: Helping other lost hikers with newfound survival skills
#             Chapter 9: Emotional reunion with worried family
#             Chapter 10: Sharing survival wisdom and inspiring others to connect with nature
#             """
#         }
#     ]
# }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', genres=list(GENRE_PLOTS.keys()))

@app.route('/get_plots/<genre>')
def get_plots(genre):
    if genre in GENRE_PLOTS:
        return jsonify(GENRE_PLOTS[genre])
    return jsonify([])

@app.route('/upload_training', methods=['POST'])
def upload_training():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4()}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/generate_book', methods=['POST'])
def generate_book():
    try:
        data = request.json
        
        # Extract form data
        child_name = data.get('child_name', '')
        child_age = data.get('child_age', '')
        child_traits = data.get('child_traits', '')
        child_interests = data.get('child_interests', '')
        genre = data.get('genre', '')
        plot_index = int(data.get('plot_index', 0))
        book_title = data.get('book_title', f"{child_name}'s Adventure")
        
        # Get selected plot
        if genre not in GENRE_PLOTS or plot_index >= len(GENRE_PLOTS[genre]):
            return jsonify({'error': 'Invalid genre or plot selection'}), 400
            
        selected_plot = GENRE_PLOTS[genre][plot_index]
        generic_outline = selected_plot['outline']
        
        # Format child info
        child_info = f"""
        Name: {child_name}
        Age: {child_age}
        Personality Traits: {child_traits}
        Interests: {child_interests}
        """
        
        # Generate the book
        from tools import generate_book
        result = generate_book(generic_outline, child_info, book_title)
        
        # Return success with book file info
        clean_title = "".join(c if c not in '<>:|"?*\\/' else '_' for c in book_title)
        filename = clean_title.replace(' ', '_')
        book_path = f"{filename}.docx"
        
        return jsonify({
            'message': 'Book generated successfully!',
            'filename': book_path,
            'preview': result[:500] + "..." if len(result) > 500 else result
        })
        
    except Exception as e:
        return jsonify({'error': f'Error generating book: {str(e)}'}), 500

@app.route('/download_book/<filename>')
def download_book(filename):
    try:
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)