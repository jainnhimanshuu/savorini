# Happy Hour Finder - API Reference

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.happyhour.ca`

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Response Format

All API responses follow a consistent format:

```json
{
  "data": <response_data>,
  "message": "Optional message",
  "meta": {
    "timestamp": "2023-12-01T12:00:00Z",
    "request_id": "req_123"
  }
}
```

### Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      "field": "Additional error context"
    }
  }
}
```

## Endpoints

### Authentication

#### POST `/v1/auth/login`

Login with email and password.

**Request:**
```json
{
  "email": "vendor@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

#### POST `/v1/auth/register`

Register a new user account.

**Request:**
```json
{
  "email": "newuser@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user"
}
```

#### GET `/v1/auth/me`

Get current user profile (requires authentication).

**Response:**
```json
{
  "data": {
    "id": "user_123",
    "email": "user@example.com",
    "role": "user",
    "first_name": "John",
    "last_name": "Doe",
    "age_verified": true,
    "created_at": "2023-12-01T12:00:00Z"
  }
}
```

### Metadata

#### GET `/v1/meta/province-rules`

Get province-specific regulatory rules.

**Response:**
```json
{
  "data": {
    "ON": {
      "province": "ON",
      "allow_price_display": true,
      "brand_logo_ok": true,
      "require_age_verification": true,
      "min_age": 19,
      "disclaimer": "Must be 19+ to consume alcohol. Please drink responsibly."
    },
    "AB": {
      "province": "AB", 
      "allow_price_display": false,
      "brand_logo_ok": true,
      "require_age_verification": true,
      "min_age": 18,
      "disclaimer": "Must be 18+ to consume alcohol. Prices subject to change."
    }
  }
}
```

#### GET `/v1/meta/cities?province=ON`

Get list of supported cities.

**Query Parameters:**
- `province` (optional): Filter by province code

**Response:**
```json
{
  "data": [
    {"name": "Toronto", "province": "ON"},
    {"name": "Ottawa", "province": "ON"},
    {"name": "Hamilton", "province": "ON"}
  ]
}
```

### Feed

#### GET `/v1/feed`

Get personalized feed of deals based on location and preferences.

**Query Parameters:**
- `lat` (required): Latitude (-90 to 90)
- `lng` (required): Longitude (-180 to 180)  
- `radius_km` (optional): Search radius in kilometers (default: 10, max: 50)
- `when` (optional): Time filter - "now", "soon", "today", "tonight" (default: "now")
- `category` (optional): Deal category filter
- `province` (optional): Province filter
- `has_food_only` (optional): Only venues serving food (default: false)
- `min_savings` (optional): Minimum savings amount
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20, max: 100)

**Response:**
```json
{
  "data": [
    {
      "deal_id": "deal_123",
      "venue_id": "venue_456", 
      "title": "$5 Wings & $4 Beer",
      "description": "Crispy wings with your choice of sauce",
      "category": "food",
      "venue_name": "The Local Pub",
      "venue_address": "123 Main St",
      "distance_km": 0.5,
      "starts_at": "15:00",
      "ends_at": "18:00", 
      "savings_amount": 8.0,
      "savings_percentage": 40.0,
      "is_featured": true,
      "image_url": "https://cdn.example.com/wings.jpg"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 45,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  },
  "when": "now",
  "location": {
    "lat": 43.6532,
    "lng": -79.3832,
    "radius_km": 10
  },
  "filters_applied": {
    "category": null,
    "province": "ON",
    "has_food_only": false,
    "min_savings": null
  }
}
```

#### GET `/v1/feed/spotlight`

Get featured/spotlight deals for homepage.

**Query Parameters:**
- `lat` (required): Latitude
- `lng` (required): Longitude
- `limit` (optional): Number of deals (default: 5, max: 10)

### Venues

#### GET `/v1/venues`

Search venues with filters.

**Query Parameters:**
- `query` (optional): Search query for name/description
- `city` (optional): City filter
- `province` (optional): Province filter
- `license_type` (optional): License type filter
- `has_food` (optional): Must serve food
- `lat`, `lng` (optional): Location for distance calculation
- `radius_km` (optional): Search radius when lat/lng provided
- `page`, `per_page`: Pagination

**Response:**
```json
{
  "data": [
    {
      "id": "venue_123",
      "name": "The Local Pub",
      "slug": "the-local-pub",
      "description": "Cozy neighborhood pub",
      "address": "123 Main St",
      "city": "Toronto", 
      "province": "ON",
      "phone": "416-555-0123",
      "website": "https://localpub.com",
      "license_type": "pub",
      "status": "active",
      "has_patio": true,
      "has_parking": false,
      "distance_km": 0.5,
      "deals_count": 3
    }
  ],
  "pagination": {...}
}
```

#### GET `/v1/venues/{venue_id}`

Get venue details by ID.

**Response:**
```json
{
  "data": {
    "id": "venue_123",
    "name": "The Local Pub",
    // ... venue fields
    "hours": [
      {
        "day": "monday",
        "open_time": "11:00",
        "close_time": "02:00",
        "is_closed": false
      }
    ],
    "secondary_hours": [
      {
        "type": "happy_hour",
        "day": "monday", 
        "start_time": "15:00",
        "end_time": "18:00"
      }
    ],
    "deals": [
      // ... current deals
    ]
  }
}
```

#### POST `/v1/venues` (Vendor)

Create new venue (requires vendor authentication).

**Request:**
```json
{
  "name": "My New Pub",
  "description": "Great atmosphere and food",
  "address": "456 Queen St",
  "city": "Toronto",
  "province": "ON", 
  "postal_code": "M5V 2B3",
  "phone": "416-555-0456",
  "email": "info@mynewpub.com",
  "website": "https://mynewpub.com",
  "license_type": "pub",
  "has_patio": true,
  "has_parking": false,
  "has_wifi": true,
  "is_accessible": true
}
```

**Response:**
```json
{
  "data": {
    "id": "venue_789"
  }
}
```

### Deals

#### GET `/v1/deals`

Search deals with filters.

**Query Parameters:**
- `venue_id` (optional): Filter by venue
- `category` (optional): Deal category
- `active_only` (optional): Only active deals (default: true)
- `featured_only` (optional): Only featured deals (default: false)
- `lat`, `lng`, `radius_km` (optional): Geographic filtering
- `page`, `per_page`: Pagination

#### GET `/v1/deals/{deal_id}`

Get deal details by ID.

#### POST `/v1/deals` (Vendor)

Create new deal (requires vendor authentication).

**Request:**
```json
{
  "venue_id": "venue_123",
  "title": "$6 Craft Beer Special",
  "description": "Local craft beers on tap",
  "category": "drink",
  "original_price": 9.00,
  "deal_price": 6.00,
  "active_days": ["monday", "tuesday", "wednesday"],
  "start_time": "16:00",
  "end_time": "19:00",
  "restrictions": "Dine-in only",
  "requires_age_verification": true
}
```

### Analytics (Vendor)

#### POST `/v1/analytics/events`

Track user interaction events.

**Request:**
```json
{
  "events": [
    {
      "type": "impression",
      "target_type": "deal", 
      "target_id": "deal_123",
      "meta": {
        "source": "feed",
        "position": 1
      }
    }
  ]
}
```

#### GET `/v1/vendor/analytics` (Vendor)

Get aggregated analytics for vendor venues.

**Query Parameters:**
- `venue_id` (optional): Specific venue
- `start_date`, `end_date`: Date range
- `metrics`: Comma-separated list of metrics

## Rate Limits

- **Public endpoints**: 100 requests per minute per IP
- **Authenticated endpoints**: 1000 requests per minute per user
- **Vendor endpoints**: 500 requests per minute per vendor

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1701432000
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `AUTHENTICATION_REQUIRED` | 401 | Missing or invalid token |
| `PERMISSION_DENIED` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

## Pagination

All list endpoints support pagination:

**Query Parameters:**
- `page`: Page number (1-based, default: 1)
- `per_page`: Items per page (default: 20, max: 100)

**Response includes pagination metadata:**
```json
{
  "pagination": {
    "page": 1,
    "per_page": 20, 
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false,
    "next_cursor": "eyJ0aW1lc3RhbXAiOiIyMDIzLTEyLTA...",
    "prev_cursor": null
  }
}
```

## Webhooks (Future)

Webhook endpoints for real-time notifications:
- Deal status changes
- Venue approval/rejection
- Analytics milestones

## SDKs

Official SDKs available for:
- JavaScript/TypeScript (npm: `@happyhour/sdk`)
- React Native (npm: `@happyhour/react-native-sdk`)
