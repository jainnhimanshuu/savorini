/**
 * Common types shared across all applications
 */

export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  meta?: Record<string, any>;
}

export interface PaginationMeta {
  page: number;
  perPage: number;
  total: number;
  pages: number;
  hasNext: boolean;
  hasPrev: boolean;
  nextCursor?: string;
  prevCursor?: string;
}

export interface PaginatedResponse<T = any> {
  data: T[];
  pagination: PaginationMeta;
  message?: string;
}

export interface ErrorDetail {
  code: string;
  message: string;
  details?: Record<string, any>;
}

export interface ErrorResponse {
  error: ErrorDetail;
}

export interface Location {
  lat: number;
  lng: number;
}

export interface Address {
  street: string;
  city: string;
  province: string;
  postalCode?: string;
  country: string;
}

export interface TimeRange {
  startTime: string; // HH:MM format
  endTime: string; // HH:MM format
}

export interface DateRange {
  startDate: string; // ISO date
  endDate: string; // ISO date
}
