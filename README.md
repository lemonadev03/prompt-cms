# Prompt CMS

A FastAPI-based Content Management System for Markdown Prompts with a clean admin interface and public API access.

## Features

- **Public API**: Access raw markdown content via UUID endpoints
- **Admin Panel**: Full CRUD operations with rich markdown editor
- **Authentication**: Session-based admin authentication
- **Database**: PostgreSQL with async SQLAlchemy
- **Migrations**: Alembic for database schema management
- **Security**: CSRF protection, security headers, input validation
- **Responsive UI**: Clean, modern admin interface

## Quick Start

### Prerequisites

- Python 3.13+
- PostgreSQL database
- uv (recommended) or pip

### Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd prompt-cms
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   # or with pip: pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env with your database credentials and admin password
   ```

4. **Setup database**:
   ```bash
   # Create database
   createdb prompt_cms
   
   # Run migrations
   alembic upgrade head
   ```

5. **Start the application**:
   ```bash
   uvicorn app.main:app --reload
   # or: python -m app.main
   ```

6. **Access the application**:
   - Admin Panel: http://localhost:8000/admin
   - API Documentation: http://localhost:8000/docs

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:password@localhost:5432/prompt_cms` |
| `ADMIN_PASSWORD` | Admin panel password | `admin123` |
| `SECRET_KEY` | Session encryption key | Auto-generated |
| `DEBUG` | Enable debug mode | `False` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## API Endpoints

### Public Endpoints

- `GET /prompt/{uuid}` - Get raw markdown content by UUID
- `GET /health` - Health check endpoint

### Admin Endpoints (Authentication Required)

- `GET /admin` - Admin dashboard
- `GET /admin/login` - Login page
- `POST /admin/login` - Handle login
- `POST /admin/logout` - Handle logout
- `GET /admin/prompt/new` - Create prompt form
- `POST /admin/prompt/new` - Handle prompt creation
- `GET /admin/prompt/{uuid}/edit` - Edit prompt form
- `POST /admin/prompt/{uuid}/edit` - Handle prompt update
- `POST /admin/prompt/{uuid}/delete` - Handle prompt deletion

## Database Schema

### Prompts Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `content` | TEXT | Markdown content |
| `description` | VARCHAR(255) | Admin description (optional) |
| `created_at` | TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | Last update timestamp |

## Usage Examples

### Creating a Prompt

1. Login to admin panel at `/admin`
2. Click "Create New Prompt"
3. Fill in description and markdown content
4. Save the prompt
5. Access via `/prompt/{uuid}`

### API Usage

```bash
# Get prompt content
curl http://localhost:8000/prompt/123e4567-e89b-12d3-a456-426614174000

# Health check
curl http://localhost:8000/health
```

### Python Client Example

```python
import requests
import uuid

# Create a prompt via admin interface first, then:
prompt_id = "your-prompt-uuid-here"
response = requests.get(f"http://localhost:8000/prompt/{prompt_id}")

if response.status_code == 200:
    markdown_content = response.text
    print(markdown_content)
else:
    print(f"Error: {response.status_code}")
```

## Development

### Project Structure

```
prompt-cms/
├── app/
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy models
│   ├── database.py      # Database configuration
│   ├── auth.py          # Authentication system
│   ├── admin.py         # Admin route handlers
│   ├── public.py        # Public route handlers
│   ├── templates/       # Jinja2 templates
│   │   ├── base.html
│   │   └── admin/
│   └── static/          # CSS and JavaScript
├── alembic/             # Database migrations
├── pyproject.toml       # Project configuration
└── README.md
```

### Running Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Development Server

```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run with debug logging
uvicorn app.main:app --reload --log-level debug
```

## Security Features

- **Session-based Authentication**: Secure admin sessions
- **CSRF Protection**: Form-based CSRF protection
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, etc.
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **XSS Protection**: Template auto-escaping

## Production Deployment

### Docker Deployment

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup

1. Set strong `ADMIN_PASSWORD`
2. Generate secure `SECRET_KEY`
3. Configure production database
4. Set `DEBUG=False`
5. Use HTTPS in production
6. Configure reverse proxy (nginx/Apache)

### Database Backup

```bash
# Backup
pg_dump prompt_cms > backup.sql

# Restore
psql prompt_cms < backup.sql
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check the documentation
- Review existing issues
- Create a new issue with detailed information
