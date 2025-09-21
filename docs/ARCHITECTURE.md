# Happy Hour Finder - Architecture

## Overview

Happy Hour Finder is a production-ready platform built with clean architecture principles, designed to help users discover happy hour deals across Canadian provinces while ensuring compliance with provincial regulations.

## System Architecture

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Mobile App    │  │  Vendor Portal  │  │  Admin Console  │
│  (React Native)│  │   (Next.js)     │  │   (Next.js)     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                    ┌─────────────────┐
                    │   Backend API   │
                    │   (FastAPI)     │
                    └─────────────────┘
                               │
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   + PostGIS     │
                    └─────────────────┘
                               │
                    ┌─────────────────┐
                    │     Redis       │
                    │   (Caching)     │
                    └─────────────────┘
```

## Application Structure

### Monorepo Layout

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
/docs               # Documentation
```

### Backend Architecture (Clean/Hexagonal)

```
apps/backend/
├── api/            # HTTP layer (routers, DTOs)
├── domain/         # Business entities and rules
├── services/       # Use cases and business logic
├── repositories/   # Data access layer
├── adapters/       # External service adapters
├── core/          # Configuration and utilities
└── migrations/    # Database migrations
```

## Key Components

### 1. Domain Layer

**Entities:**
- `User` - System users (consumers, vendors, admins)
- `Venue` - Physical locations with licensing info
- `Deal` - Happy hour offers with compliance rules
- `ProvinceRule` - Regulatory compliance per province
- `Hours` - Operating hours (regular + secondary)
- `Media` - Images, menus, logos

**Value Objects:**
- Location coordinates (PostGIS Point)
- Time ranges
- Price display modes

### 2. Service Layer

**Core Services:**
- `ComplianceService` - Province-specific rule enforcement
- `VenueService` - Venue management and search
- `DealService` - Deal CRUD and filtering
- `SearchService` - Geographic and text search
- `ModerationService` - Content review workflows
- `AnalyticsService` - Event tracking and metrics

### 3. Data Layer

**Primary Database (PostgreSQL + PostGIS):**
- Spatial indexing for geographic queries
- Full-text search capabilities
- ACID compliance for transactional data

**Cache Layer (Redis):**
- Feed caching with geographic keys
- Session storage
- Rate limiting counters

## Request Flow

### 1. Feed Request Flow

```
Mobile App → API Gateway → Feed Router → Search Service
                                      ↓
Cache Check → Compliance Service → Database Query
     ↓              ↓                    ↓
   Hit: Return   Apply Rules         PostGIS Query
     ↓              ↓                    ↓
   Miss: Query → Format Response ← Venue + Deal Join
```

### 2. Venue Creation Flow

```
Vendor Portal → Auth Middleware → Venue Router → Venue Service
                                                      ↓
                                               Validation Rules
                                                      ↓
                                               Geocoding Service
                                                      ↓
                                               Database Insert
                                                      ↓
                                               Moderation Queue
```

## Performance Optimizations

### 1. Database Optimizations

- **Spatial Indexes**: PostGIS GIST indexes on venue locations
- **Composite Indexes**: `(venue_id, is_active)`, `(province, status)`
- **Covering Indexes**: Include frequently accessed columns
- **Partial Indexes**: Only on active records

### 2. Caching Strategy

```
Cache Key Pattern: feed:{province}:{grid_cell}:{time_bucket}
TTL: 60-300 seconds based on volatility
Invalidation: On venue updates, deal modifications
```

### 3. API Optimizations

- **Async Everything**: FastAPI + async SQLAlchemy
- **Connection Pooling**: 20 base, 30 overflow connections  
- **Bulk Operations**: Batch inserts and updates
- **Pagination**: Cursor-based for large datasets
- **ETags**: Cache validation for read endpoints

## Security Architecture

### 1. Authentication & Authorization

- **JWT Tokens**: Access (30min) + Refresh (7 days)
- **Role-Based Access**: User, Vendor, Admin roles
- **Scope-Based Permissions**: Fine-grained API access

### 2. Data Protection

- **Input Validation**: Pydantic schemas at API boundary
- **SQL Injection**: SQLAlchemy ORM protection
- **Rate Limiting**: Per-IP and per-user limits
- **Audit Logging**: All admin and vendor actions

### 3. Compliance Features

- **Province Rules Engine**: Dynamic compliance checking
- **Age Verification**: Required for alcohol-related deals
- **Price Display Controls**: Hide/show/redact based on regulations
- **Content Moderation**: Automated and manual review workflows

## Scalability Considerations

### 1. Horizontal Scaling

- **Stateless API**: No server-side sessions
- **Database Read Replicas**: For read-heavy workloads
- **Redis Clustering**: For cache distribution
- **CDN Integration**: For media assets

### 2. Geographic Distribution

- **Multi-Region Deployment**: Reduce latency
- **Geographic Sharding**: Province-based data partitioning
- **Edge Caching**: Location-aware cache distribution

## Monitoring & Observability

### 1. Logging

- **Structured Logging**: JSON format with correlation IDs
- **Log Levels**: DEBUG, INFO, WARN, ERROR with appropriate filtering
- **Request Tracing**: End-to-end request correlation

### 2. Metrics

- **Business Metrics**: Deal views, venue engagement, conversion rates
- **System Metrics**: Response times, error rates, throughput
- **Infrastructure Metrics**: Database connections, cache hit rates

### 3. Alerting

- **Error Rate Thresholds**: >1% error rate alerts
- **Performance Degradation**: >500ms P95 response time
- **Business Anomalies**: Unusual drop in deal interactions

## Technology Choices

### Backend Stack

- **FastAPI**: Modern, fast, async-first Python framework
- **SQLAlchemy 2.0**: Modern ORM with async support
- **Pydantic v2**: Fast data validation and serialization
- **PostGIS**: Spatial database capabilities
- **Redis**: High-performance caching and sessions

### Frontend Stack

- **Next.js 14**: App Router for modern React development
- **React Native/Expo**: Cross-platform mobile development
- **TypeScript**: Type safety across the entire stack
- **Tailwind CSS**: Utility-first styling system

### Infrastructure

- **Docker Compose**: Local development environment
- **12-Factor App**: Environment-based configuration
- **CI/CD Ready**: GitHub Actions workflows included
