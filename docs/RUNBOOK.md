# Happy Hour Finder - Runbook

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.12+ (for local development)
- Git

### One-Command Setup

```bash
# Clone the repository
git clone <repository-url>
cd savorini

# Start all services
make up
```

**Services will be available at:**
- Backend API: http://localhost:8000/docs
- Vendor Portal: http://localhost:3000  
- Admin Console: http://localhost:3001
- Mobile (Expo): http://localhost:8081
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Development Workflows

### Backend Development

```bash
# Start backend only
cd apps/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]

# Set up database
createdb happyhour
alembic upgrade head

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# Vendor Portal
cd apps/web-vendor
npm install
npm run dev

# Admin Console  
cd apps/web-admin
npm install
npm run dev

# Mobile App
cd apps/mobile
npm install
npx expo start
```

### Database Management

```bash
# Create migration
cd apps/backend
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Reset database (DESTRUCTIVE)
make db.reset
```

### Seeding Data

```bash
# Load sample data
make seed

# Or manually:
cd apps/backend
python -m ops.scripts.seed
```

## Environment Configuration

### Local Development (.env)

```bash
# Copy example environment
cp env.example .env

# Edit with your values
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/happyhour
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-super-secret-key-change-in-production
```

### Required Environment Variables

**Backend:**
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string  
- `JWT_SECRET_KEY`: Secret for JWT token signing
- `GOOGLE_PLACES_API_KEY`: For address geocoding
- `SENDGRID_API_KEY`: For email notifications

**Frontend:**
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXTAUTH_SECRET`: NextAuth.js secret
- `NEXTAUTH_URL`: Application base URL

**Mobile:**
- `EXPO_PUBLIC_API_URL`: Backend API URL
- `EXPO_ACCESS_TOKEN`: For EAS builds

## Testing

### Backend Tests

```bash
cd apps/backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/services/test_compliance_service.py

# Run integration tests
pytest tests/api/

# Run unit tests only
pytest tests/services/ tests/domain/
```

### Frontend Tests

```bash
# Vendor Portal
cd apps/web-vendor
npm test
npm run test:watch

# Mobile App
cd apps/mobile  
npm test
```

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Get feed (requires location)
curl "http://localhost:8000/v1/feed?lat=43.6532&lng=-79.3832"

# Login
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"vendor@example.com","password":"password"}'
```

## Debugging

### Backend Debugging

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# View logs
docker-compose logs -f backend

# Database queries
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/happyhour?echo=true"

# Interactive shell
docker-compose exec backend python -c "
from core.database import init_database
import asyncio
asyncio.run(init_database())
"
```

### Database Debugging

```bash
# Connect to database
make shell.db

# Or with docker
docker-compose exec postgres psql -U postgres -d happyhour

# Common queries
SELECT COUNT(*) FROM venues WHERE status = 'active';
SELECT province, COUNT(*) FROM venues GROUP BY province;
```

### Redis Debugging

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# View cache keys
KEYS feed:*
GET feed:ON:grid_123:bucket_456

# Monitor commands
MONITOR
```

## Performance Monitoring

### Database Performance

```sql
-- Slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Index usage
SELECT schemaname, tablename, indexname, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes 
ORDER BY idx_tup_read DESC;

-- Table sizes
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(tablename::regclass)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;
```

### Application Metrics

```bash
# Backend metrics endpoint
curl http://localhost:8000/metrics

# Cache hit rates
docker-compose exec redis redis-cli INFO stats

# Connection pool status
curl http://localhost:8000/health/detailed
```

## Troubleshooting

### Common Issues

**1. Database Connection Errors**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check connection from backend
docker-compose exec backend python -c "
import asyncpg
import asyncio
async def test():
    conn = await asyncpg.connect('postgresql://postgres:postgres@postgres:5432/happyhour')
    await conn.close()
    print('Connection successful')
asyncio.run(test())
"
```

**2. Redis Connection Errors**
```bash
# Check Redis status
docker-compose exec redis redis-cli ping

# Check from backend
docker-compose exec backend python -c "
import redis
r = redis.from_url('redis://redis:6379/0')
print(r.ping())
"
```

**3. Frontend Build Errors**
```bash
# Clear Next.js cache
cd apps/web-vendor
rm -rf .next node_modules
npm install
npm run build

# Clear Expo cache
cd apps/mobile
npx expo start --clear
```

**4. Migration Errors**
```bash
# Check current migration state
cd apps/backend
alembic current

# Check pending migrations
alembic heads

# Force migration state (dangerous)
alembic stamp head
```

### Log Analysis

```bash
# View all logs
docker-compose logs

# Follow specific service
docker-compose logs -f backend

# Search logs
docker-compose logs backend | grep ERROR

# View structured logs
docker-compose logs backend | jq '.message'
```

## Deployment

### Production Checklist

**Security:**
- [ ] Change all default passwords
- [ ] Set strong JWT_SECRET_KEY
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable audit logging

**Performance:**
- [ ] Set up database connection pooling
- [ ] Configure Redis clustering
- [ ] Enable CDN for static assets
- [ ] Set up monitoring and alerting
- [ ] Configure log aggregation

**Reliability:**
- [ ] Set up database backups
- [ ] Configure health checks
- [ ] Set up auto-scaling
- [ ] Test disaster recovery
- [ ] Document rollback procedures

### Environment-Specific Configs

**Staging:**
```bash
export ENVIRONMENT=staging
export DEBUG=false
export LOG_LEVEL=INFO
export DATABASE_URL=postgresql+asyncpg://user:pass@staging-db:5432/happyhour
```

**Production:**
```bash
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=WARNING
export DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/happyhour
export SENTRY_DSN=https://your-sentry-dsn
```

## Maintenance

### Database Maintenance

```bash
# Vacuum and analyze
docker-compose exec postgres psql -U postgres -d happyhour -c "VACUUM ANALYZE;"

# Reindex
docker-compose exec postgres psql -U postgres -d happyhour -c "REINDEX DATABASE happyhour;"

# Backup
docker-compose exec postgres pg_dump -U postgres happyhour > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres happyhour < backup.sql
```

### Cache Maintenance

```bash
# Clear all cache
docker-compose exec redis redis-cli FLUSHALL

# Clear specific patterns
docker-compose exec redis redis-cli --eval "
for i, name in ipairs(redis.call('KEYS', ARGV[1])) do
  redis.call('DEL', name);
end" 0 feed:*
```

### Log Rotation

```bash
# Rotate Docker logs
docker-compose down
docker system prune -f
docker-compose up -d
```

## Support

### Getting Help

1. Check this runbook first
2. Search existing issues in the repository
3. Check application logs for error details
4. Create a new issue with:
   - Environment details
   - Steps to reproduce
   - Error messages
   - Relevant logs

### Useful Commands Reference

```bash
# Quick status check
make status

# View all services
docker-compose ps

# Restart specific service
docker-compose restart backend

# View resource usage
docker stats

# Clean up everything
make clean
```
