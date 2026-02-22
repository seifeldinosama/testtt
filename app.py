from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def generate_dockerfile(python_version='3.9', port=5000, requirements=None):
    """Generate a Dockerfile content for a Python application"""
    if requirements is None:
        requirements = []
    
    dockerfile_content = f"""FROM python:{python_version}-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE {port}

CMD ["python", "app.py"]
"""
    return dockerfile_content

def save_dockerfile(content, filename='Dockerfile'):
    """Save the Dockerfile to the current directory"""
    with open(filename, 'w') as f:
        f.write(content)
    return filename

@app.route('/create-dockerfile', methods=['POST'])
def create_dockerfile():
    """API endpoint to create a Dockerfile"""
    data = request.get_json()
    
    # Get parameters with defaults
    python_version = data.get('python_version', '3.9')
    port = data.get('port', 5000)
    requirements = data.get('requirements', [])
    
    # Generate Dockerfile content
    dockerfile_content = generate_dockerfile(python_version, port, requirements)
    
    # Save to file
    filename = save_dockerfile(dockerfile_content)
    
    return jsonify({
        'message': 'Dockerfile created successfully',
        'filename': filename,
        'content': dockerfile_content
    })

@app.route('/generate', methods=['GET'])
def generate_simple():
    """Simple GET endpoint to generate a basic Dockerfile"""
    dockerfile_content = generate_dockerfile()
    return dockerfile_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
