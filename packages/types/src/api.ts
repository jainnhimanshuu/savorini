/**
 * API request/response types
 */

import {
  DealCategory,
  DayOfWeek,
  LicenseType,
  Province,
  UserRole,
} from "./domain";

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role?: UserRole;
}

export interface TokenResponse {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
  expiresIn: number;
}

// Feed types
export interface FeedFilters {
  lat: number;
  lng: number;
  radiusKm?: number;
  when?: "now" | "soon" | "today" | "tonight";
  category?: DealCategory;
  province?: Province;
  hasFoodOnly?: boolean;
  minSavings?: number;
}

export interface FeedItem {
  dealId: string;
  venueId: string;
  title: string;
  description?: string;
  category: DealCategory;
  venueName: string;
  venueAddress: string;
  distanceKm: number;
  startsAt?: string;
  endsAt?: string;
  savingsAmount?: number;
  savingsPercentage?: number;
  isFeatured: boolean;
  imageUrl?: string;
}

// Venue types
export interface VenueCreateRequest {
  name: string;
  description?: string;
  address: string;
  city: string;
  province: Province;
  postalCode?: string;
  phone?: string;
  email?: string;
  website?: string;
  licenseType: LicenseType;
  hasPatio?: boolean;
  hasParking?: boolean;
  hasWifi?: boolean;
  isAccessible?: boolean;
}

export interface VenueUpdateRequest {
  name?: string;
  description?: string;
  address?: string;
  city?: string;
  province?: Province;
  postalCode?: string;
  phone?: string;
  email?: string;
  website?: string;
  licenseType?: LicenseType;
  hasPatio?: boolean;
  hasParking?: boolean;
  hasWifi?: boolean;
  isAccessible?: boolean;
}

export interface VenueSearchFilters {
  query?: string;
  city?: string;
  province?: Province;
  licenseType?: LicenseType;
  hasFood?: boolean;
  lat?: number;
  lng?: number;
  radiusKm?: number;
  page?: number;
  perPage?: number;
}

// Deal types
export interface DealCreateRequest {
  venueId: string;
  title: string;
  description?: string;
  category: DealCategory;
  originalPrice?: number;
  dealPrice?: number;
  activeDays: DayOfWeek[];
  startTime?: string;
  endTime?: string;
  restrictions?: string;
  terms?: string;
  minPurchase?: number;
  maxRedemptions?: number;
  requiresAgeVerification?: boolean;
}

export interface DealUpdateRequest {
  title?: string;
  description?: string;
  category?: DealCategory;
  originalPrice?: number;
  dealPrice?: number;
  activeDays?: DayOfWeek[];
  startTime?: string;
  endTime?: string;
  restrictions?: string;
  terms?: string;
  minPurchase?: number;
  maxRedemptions?: number;
  requiresAgeVerification?: boolean;
  isActive?: boolean;
}

export interface DealSearchFilters {
  venueId?: string;
  category?: DealCategory;
  activeOnly?: boolean;
  featuredOnly?: boolean;
  lat?: number;
  lng?: number;
  radiusKm?: number;
  page?: number;
  perPage?: number;
}

// Media types
export interface MediaUploadRequest {
  venueId: string;
  type: "image" | "menu" | "logo";
  filename: string;
  contentType: string;
  fileSize: number;
  altText?: string;
  caption?: string;
}

export interface MediaUploadResponse {
  uploadUrl: string;
  mediaId: string;
  expiresAt: string;
}

// Analytics types
export interface AnalyticsEvent {
  type:
    | "impression"
    | "click"
    | "save"
    | "unsave"
    | "flag"
    | "share"
    | "call"
    | "directions"
    | "website_visit";
  targetType?: "deal" | "venue";
  targetId: string;
  meta?: Record<string, any>;
}

export interface AnalyticsMetrics {
  impressions: number;
  clicks: number;
  saves: number;
  shares: number;
  conversionRate: number;
  topCategories: Array<{
    category: DealCategory;
    count: number;
  }>;
  topTimes: Array<{
    hour: number;
    count: number;
  }>;
}
