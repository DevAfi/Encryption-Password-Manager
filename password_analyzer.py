import re

def calculate_strength(password: str) -> dict:
    has_seq = False
    score = 0
    if is_password_common(password):
        return {
        'score': 0,
        'rating': 'very weak',
        'is_common': True,
        'has_seq': False
        }
        


    

    length = len(password)
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 30
    elif length >= 8:
        score += 20
    else:
        score+= 10

    if has_seq_chars:
        has_seq = True
        score -= 20


    score = max(0, score)


    if re.search(r'[a-z]', password):  # Has lowercase
        score += 15
    if re.search(r'[A-Z]', password):  # Has uppercase
        score += 15
    if re.search(r'[0-9]', password):  # Has numbers
        score += 15
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Has symbols
        score += 15
    
    # Determine rating based on score
    if score >= 80:
        rating = 'very strong'
    elif score >= 60:
        rating = 'strong'
    elif score >= 40:
        rating = 'medium'
    else:
        rating = 'weak'
    
    return {
        'score': score,
        'rating': rating,
        'is_common': False,
        'has_seq': has_seq
    }

def load_common_passwords() -> set:
    try:
        with open('common_passwords.txt', 'r') as f:
            passwords = {line.strip().lower() for line in f if line.strip()}
            return passwords
    except FileNotFoundError:
        print("File not found")
        return set()
    
def is_password_common(password: str) -> bool:
    common = load_common_passwords()
    return password.lower() in common

def has_seq_chars(password: str) -> bool:
    password = password.lower()

    sequences = [
        'qwertyuiop',
        'asdfghjkl',
        'zxcvbnm'
        'abcdefghijklmnopqrstuvwxyz',
        '1234567890'
    ]

    for seq in sequences:
        for i in range(len(seq) - 2):
            substring = seq[i:i+3]
            if substring in password:
                return True
            # Backward sequence (e.g., "cba", "321")
            if substring[::-1] in password:
                return True
    
    return False

def get_feedback(password: str) -> list:
    feedback = []
    
    # Check if it's a common password
    if is_password_common(password):
        feedback.append("This is a commonly used password - choose something unique")
        return feedback  # If common, other feedback doesn't matter
    
    # Length feedback
    length = len(password)
    if length < 8:
        feedback.append("!  Password is too short - use at least 8 characters (12+ recommended)")
    elif length < 12:
        feedback.append("!  Consider making it longer (12+ characters is better)")
    
    # Character variety feedback
    if not re.search(r'[a-z]', password):
        feedback.append("+  Add lowercase letters (a-z)")
    if not re.search(r'[A-Z]', password):
        feedback.append("+  Add uppercase letters (A-Z)")
    if not re.search(r'[0-9]', password):
        feedback.append("+  Add numbers (0-9)")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        feedback.append("+  Add special symbols (!@#$%^&*)")
    
    # Pattern feedback
    if has_seq_chars(password):
        feedback.append("!  Avoid sequential characters (abc, 123, qwerty)")
    
    # If no feedback, it's strong!
    if not feedback:
        feedback.append("✓ Strong password! No improvements needed.")
    
    return feedback

def display_strength_analysis(password: str):
    result = calculate_strength(password)
    feedback = get_feedback(password)
    
    print("\n" + "="*50)
    print("PASSWORD STRENGTH ANALYSIS")
    print("="*50)
    print(f"Score:   {result['score']}/100")
    print(f"Rating:  {result['rating'].upper()}")
    print("\nFeedback:")
    for item in feedback:
        print(f"  {item}")
    print("="*50)