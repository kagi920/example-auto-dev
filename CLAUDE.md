# Claude Code Project Configuration

## Project Overview
This is a Flask-based web application for user authentication and management.

## Development Workflow
- Issues are created using `gh issue create`
- Implementation is automated using `./auto-dev.sh`
- CI runs on pull requests with pytest tests
- Use `git checkout main && git pull` to stay up to date

## Commands
- **Test**: `pytest`
- **Lint**: Not configured yet
- **Run**: `python main.py`
- **Install**: `pip install -r requirements.txt`

## Project Structure
- `main.py` - Flask application with user registration API
- `test_main.py` - Pytest tests for the API
- `.github/workflows/ci.yml` - CI workflow
- `requirements.txt` - Python dependencies
- `auto-dev.sh` - Automated development script

## Current Features
- POST /signup API endpoint for user registration
- SQLite database for user storage
- Password hashing with SHA-256
- Basic form validation
- CI/CD with GitHub Actions