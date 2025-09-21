/**
 * Domain types matching backend entities
 */

// Enums
export enum UserRole {
  USER = "user",
  VENDOR = "vendor",
  ADMIN = "admin",
}

export enum VenueStatus {
  PENDING = "pending",
  ACTIVE = "active",
  SUSPENDED = "suspended",
  INACTIVE = "inactive",
}

export enum LicenseType {
  RESTAURANT = "restaurant",
  BAR = "bar",
  PUB = "pub",
  BREWERY = "brewery",
  WINERY = "winery",
  DISTILLERY = "distillery",
  NIGHTCLUB = "nightclub",
  LOUNGE = "lounge",
}

export enum DayOfWeek {
  MONDAY = "monday",
  TUESDAY = "tuesday",
  WEDNESDAY = "wednesday",
  THURSDAY = "thursday",
  FRIDAY = "friday",
  SATURDAY = "saturday",
  SUNDAY = "sunday",
}

export enum SecondaryHoursType {
  HAPPY_HOUR = "happy_hour",
  LATE_NIGHT = "late_night",
  BRUNCH = "brunch",
  PATIO = "patio",
  KITCHEN = "kitchen",
}

export enum DealCategory {
  FOOD = "food",
  DRINK = "drink",
  BUNDLE = "bundle",
  EVENT = "event",
}

export enum PriceDisplayMode {
  HIDE = "hide",
  SHOW = "show",
  REDACT = "redact",
}

export enum MediaType {
  IMAGE = "image",
  MENU = "menu",
  LOGO = "logo",
}

export enum Province {
  ON = "ON",
  BC = "BC",
  AB = "AB",
  QC = "QC",
  NS = "NS",
  NB = "NB",
  MB = "MB",
  SK = "SK",
  PE = "PE",
  NL = "NL",
  YT = "YT",
  NT = "NT",
  NU = "NU",
}

// Domain entities
export interface User {
  id: string;
  email: string;
  role: UserRole;
  firstName?: string;
  lastName?: string;
  phone?: string;
  ageVerified: boolean;
  isActive: boolean;
  createdAt: string;
  lastLoginAt?: string;
}

export interface Venue {
  id: string;
  name: string;
  slug?: string;
  description?: string;
  address: string;
  city: string;
  province: Province;
  postalCode?: string;
  phone?: string;
  email?: string;
  website?: string;
  licenseType: LicenseType;
  vendorId: string;
  status: VenueStatus;
  hasPatio: boolean;
  hasParking: boolean;
  hasWifi: boolean;
  isAccessible: boolean;
  googlePlaceId?: string;
  lastVerifiedAt?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Hours {
  venueId: string;
  day: DayOfWeek;
  openTime?: string;
  closeTime?: string;
  isClosed: boolean;
}

export interface SecondaryHours {
  venueId: string;
  type: SecondaryHoursType;
  day: DayOfWeek;
  startTime: string;
  endTime: string;
  isActive: boolean;
}

export interface Deal {
  id: string;
  venueId: string;
  title: string;
  description?: string;
  category: DealCategory;
  originalPrice?: number;
  dealPrice?: number;
  priceDisplayMode: PriceDisplayMode;
  activeDays: DayOfWeek[];
  startTime?: string;
  endTime?: string;
  restrictions?: string;
  terms?: string;
  minPurchase?: number;
  maxRedemptions?: number;
  redemptionsUsed: number;
  isActive: boolean;
  isFeatured: boolean;
  requiresAgeVerification: boolean;
  lastVerifiedAt?: string;
  verifiedBy?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Media {
  id: string;
  venueId: string;
  type: MediaType;
  uri: string;
  altText?: string;
  caption?: string;
  filename?: string;
  fileSize?: number;
  mimeType?: string;
  width?: number;
  height?: number;
  isPrimary: boolean;
  displayOrder: number;
  isActive: boolean;
  uploadedBy: string;
  createdAt: string;
  updatedAt: string;
}

export interface ProvinceRule {
  province: Province;
  allowPriceDisplay: boolean;
  brandLogoOk: boolean;
  disclaimer?: string;
  requireAgeVerification: boolean;
  minAge: number;
  hideAlcoholBrands: boolean;
  hideAlcoholPrices: boolean;
  requireFoodWithAlcohol: boolean;
  alcoholSalesStartTime?: string;
  alcoholSalesEndTime?: string;
  allowHappyHourMarketing: boolean;
  maxDiscountPercentage?: number;
  createdAt: string;
  updatedAt: string;
}

// Composite types
export interface VenueWithDetails extends Venue {
  hours: Hours[];
  secondaryHours: SecondaryHours[];
  dealsCount: number;
  distanceKm?: number;
}

export interface DealWithVenue extends Deal {
  venueName: string;
  venueAddress: string;
  venueCity: string;
  venueProvince: string;
  distanceKm?: number;
  savingsAmount?: number;
  savingsPercentage?: number;
}
