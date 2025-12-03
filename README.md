# IncognitoChat

A Flask-based real-time chat and blog application with user authentication, post creation, and commenting system using WebSockets.

## Features

- 🔐 **User Authentication** - Secure login and registration system
- 💬 **Real-time Chat** - WebSocket-based instant messaging with Flask-SocketIO
- 📝 **Blog Posts** - Create, read, and share blog posts
- 💭 **Comments** - Comment on posts and engage with other users
- 👤 **User Profiles** - User management and authentication
- 🎨 **Bootstrap UI** - Responsive Bootstrap-based interface
- 📱 **Mobile Friendly** - Works on desktop and mobile devices

## Tech Stack

- **Backend:** Flask 3.0.2
- **Database:** SQLite (SQLAlchemy ORM)
- **Real-time:** Flask-SocketIO with WebSockets
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF with WTForms
- **UI:** Bootstrap 3.3.7.1
- **Server:** Gunicorn

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sama-ndari/IncognitoChat.git
cd IncognitoChat
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
DEBUG=True
DATABASE_URL=sqlite:///chat.db
```

### 5. Initialize Database

```bash
python main.py
```

The database will be created automatically on first run.

### 6. Run the Application

```bash
python main.py
```

Visit: **http://localhost:5000**

## Project Structure

```
IncognitoChat/
├── main.py                 # Flask app, routes, models
├── forms.py                # WTForms for login, registration, posts
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── Procfile                # Heroku deployment config
├── poetry.lock             # Poetry lock file
├── pyproject.toml          # Poetry config
├── templates/              # HTML templates
│   ├── index.html          # Home page
│   ├── header.html         # Navigation header
│   ├── footer.html         # Footer
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── all_posts.html      # All posts listing
│   ├── post.html           # Single post view
│   ├── refresh.html        # Refresh page
│   └── looser.html         # Access denied page
├── static/                 # Static files (CSS, JS, images)
└── instance/               # Instance folder (created at runtime)
    └── chat.db             # SQLite database
```

## Database Schema

### User Table

- `id` - Primary key
- `name` - Username (unique)
- `password` - Hashed password
- `posts` - Relationship to posts
- `comments` - Relationship to comments

### Post Table

- `id` - Primary key
- `title` - Post title
- `subtitle` - Post subtitle
- `timestamp` - Creation timestamp
- `user_id` - Foreign key to User
- `author` - Relationship to User
- `comments` - Relationship to comments

### Comment Table

- `id` - Primary key
- `content` - Comment text
- `timestamp` - Creation timestamp
- `user_id` - Foreign key to User
- `post_id` - Foreign key to Post
- `commenter` - Relationship to User
- `parent_post` - Relationship to Post

## Usage

### Register a New Account

1. Click "Register" on the home page
2. Enter username and password
3. Click "Register"

### Login

1. Click "Login" on the home page
2. Enter credentials
3. Click "Login"

### Create a Post

1. After login, navigate to "New Post"
2. Enter title and subtitle
3. Click "Create Post"

### Comment on Posts

1. View a post
2. Scroll to comments section
3. Enter comment and click "Post Comment"

### Real-time Chat

- Open the chat interface
- Messages are delivered in real-time via WebSockets
- See other users' messages instantly

## API Routes

### Authentication

- `GET /` - Home page
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Posts

- `GET /all-posts` - View all posts
- `GET /post/<id>` - View single post
- `POST /new-post` - Create new post
- `POST /edit-post/<id>` - Edit post
- `POST /delete-post/<id>` - Delete post

### Comments

- `POST /comment/<post_id>` - Add comment to post
- `POST /delete-comment/<comment_id>` - Delete comment

## WebSocket Events

Real-time communication using Flask-SocketIO:

- `connect` - User connects to chat
- `disconnect` - User disconnects
- `message` - Send/receive messages
- `typing` - User typing indicator

## Environment Variables

| Variable       | Description                          | Default           |
| -------------- | ------------------------------------ | ----------------- |
| `SECRET_KEY`   | Flask secret key                     | dev-secret-key    |
| `FLASK_ENV`    | Environment (development/production) | development       |
| `DEBUG`        | Debug mode                           | True              |
| `DATABASE_URL` | Database connection string           | sqlite:///chat.db |

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Activate virtual environment and install dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Secret key not set"

**Solution:** Create `.env` file with `SECRET_KEY`

```bash
cp .env.example .env
# Edit .env and add SECRET_KEY
```

### Issue: Database locked

**Solution:** Delete the database and restart

```bash
rm instance/chat.db
python main.py
```

### Issue: Port 5000 already in use

**Solution:** Change port in main.py

```python
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
```

## Deployment

### Heroku Deployment

1. Install Heroku CLI
2. Login to Heroku: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your_secret_key
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```

The `Procfile` is already configured for Heroku deployment.

## Security Notes

- Never commit `.env` file to version control
- Change `SECRET_KEY` in production
- Use strong passwords
- Enable HTTPS in production
- Validate all user inputs
- Use CSRF protection (Flask-WTF handles this)

## Dependencies

- Flask 3.0.2 - Web framework
- Flask-SQLAlchemy 3.1.1 - ORM
- Flask-Login 0.6.3 - Authentication
- Flask-SocketIO 5.3.6 - WebSockets
- Flask-WTF 1.2.1 - Form handling
- Flask-Bootstrap 3.3.7.1 - UI framework
- SQLAlchemy 2.0.27 - Database ORM
- Werkzeug 3.0.1 - WSGI utilities
- WTForms 3.1.2 - Form validation
- Gunicorn 21.2.0 - Production server

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is part of the 100 Days of Code challenge.

## Support

For issues or questions:

1. Check the Troubleshooting section
2. Review the code comments
3. Check Flask and Flask-SocketIO documentation
4. Open an issue on GitHub

---

**Last Updated:** December 2025
**Python Version:** 3.8+
**Flask Version:** 3.0.2
