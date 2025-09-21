# Happy Hour Finder (Canada) 🍻

A production-ready platform for discovering happy hour deals across Canadian provinces.

## Architecture

- **Mobile App**: React Native (Expo) for iOS/Android consumers
- **Web Portals**: Next.js (Vendor Portal + Admin Console)  
- **Backend**: FastAPI (async), PostgreSQL + PostGIS, Redis
- **Infrastructure**: Docker Compose for local development

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd savorini

# Start all services
make up

# Access services
- Backend API: http://localhost:8000/docs
- Vendor Portal: http://localhost:3000
- Admin Console: http://localhost:3001
- Mobile (Expo): http://localhost:8081
```

## Project Structure

```
/apps
  /backend          # FastAPI backend
  /web-vendor       # Next.js vendor portal
  /web-admin        # Next.js admin console
  /mobile           # Expo React Native app
/packages
  /ui               # Shared design system
  /types            # Shared TypeScript types
/ops                # Docker, CI/CD, scripts
```

## Development

```bash
# Database migrations
make db.migrate

# Run tests
make test

# Lint and format
make lint

# Seed data
make seed
```

## Documentation

- [Architecture](./docs/ARCHITECTURE.md)
- [API Reference](./docs/API.md)
- [Database Schema](./docs/SCHEMA.sql)
- [Runbook](./docs/RUNBOOK.md)
- [Security](./docs/SECURITY.md)
- [Performance](./docs/PERF.md)

## License

MIT
