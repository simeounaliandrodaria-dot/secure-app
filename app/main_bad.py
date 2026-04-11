import pytest
import json
from app.main_bad import app

# BUG: The validation function is intentionally flawed
def is_valid_url(url):
    """Validate URL format to prevent SSRF."""
    try:
        result = urlparse(url)
        # BUG: Missing check for valid schemes, allowing 'file://' and others
        return all([result.scheme, result.netloc])
    except:
        return False

# BUG: Insufficient sanitization for SQL-like injection patterns
def sanitize_input(user_input):
    """Basic input sanitization to prevent injection attacks."""
    # BUG: Only removes angle brackets, leaving other dangerous chars like '; --'
    return re.sub(r'[<>]', '', user_input)

# ... (rest of the app is the same as good branch) ...

@app.route('/greet', methods=['GET'])
def greet():
    """Secure greeting endpoint with input validation."""
    name = request.args.get('name', 'World')
    
    # Input validation and sanitization
    if name:
        # BUG: Missing length check, allowing potential buffer issues
        name = sanitize_input(name)
    
    return jsonify({"message": f"Hello, {name}!"})
