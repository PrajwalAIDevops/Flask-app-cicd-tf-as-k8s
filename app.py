from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# Track server start time for the health check uptime calculation
START_TIME = time.time()

# --------------------------------------------------------------------
# 1. FRONTEND ROUTE
# --------------------------------------------------------------------
@app.route('/')
def index():
    """Renders the main dashboard user interface."""
    return render_template('index.html')


# --------------------------------------------------------------------
# 2. FEATURE ENDPOINTS (3 Required Endpoints)
# --------------------------------------------------------------------

@app.route('/api/submit', methods=['POST'])
def handle_submit():
    """Endpoint 1: Processes user registration/onboarding submissions."""
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({
            'status': 'error',
            'message': 'Please provide a valid name.'
        }), 400
        
    return jsonify({
        'status': 'success',
        'message': f'Welcome aboard, {username}! Your session has started successfully.'
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Endpoint 2: Simulates fetching live dashboard metric widgets."""
    # In a real app, this data would come from a database
    dashboard_metrics = {
        'active_users': 1420,
        'server_load_percentage': 24.5,
        'total_requests_today': 8912,
        'status': 'optimized'
    }
    return jsonify({
        'status': 'success',
        'data': dashboard_metrics
    })


@app.route('/api/toggle-theme', methods=['POST'])
def toggle_theme():
    """Endpoint 3: Saves user UI preferences (e.g., dark mode toggle)."""
    data = request.get_json() or {}
    preferred_theme = data.get('theme', 'dark')
    
    return jsonify({
        'status': 'success',
        'message': f'UI configuration updated to {preferred_theme} mode.',
        'applied_theme': preferred_theme
    })


# --------------------------------------------------------------------
# 3. HEALTH CHECK ENDPOINT
# --------------------------------------------------------------------
@app.route('/health', methods=['GET'])
def health_check():
    """
    Standardized API health check endpoint.
    Used by load balancers, Docker, or Kubernetes to monitor application status.
    """
    uptime_seconds = round(time.time() - START_TIME, 2)
    
    health_status = {
        'status': 'healthy',              # Options: 'healthy', 'unhealthy', 'degraded'
        'timestamp': time.time(),
        'uptime_seconds': uptime_seconds,
        'services': {
            'database': 'connected',      # Mock dependency checks
            'cache_redis': 'operational'
        }
    }
    
    # Returns HTTP 200 OK for a healthy system status
    return jsonify(health_status), 200


if __name__ == '__main__':
    # Force the reloader to ignore anything outside your current project directory
    app.run(host='0.0.0.0', port=5000, debug=True)