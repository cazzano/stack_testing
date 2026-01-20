/**
 * Parser for Policy Uses API data
 * Handles usage, english preference, and description fields
 */

export interface UsageItem {
  website?: string;
  "mobile app"?: string;
  "facebook application"?: string;
}

export interface ParsedUsage {
  usage: UsageItem[];
}

export interface ParsedEnglishPreference {
  "english preference": string;
}

export interface DescriptionItem {
  confirmation: string;
  use_case: string;
  description: string;
}

export interface ParsedDescription {
  "use and description": DescriptionItem[];
}

/**
 * Parse usage field
 * Format: "website_mobile app_facebook application"
 * - Items are separated by _ (underscore)
 *
 * Example: "hello world.com_health care app_facebook app"
 */
export function parseUsage(raw: string | null): ParsedUsage {
  if (!raw || !raw.trim()) {
    return { usage: [] };
  }

  const parts = raw.trim().split('_').map(p => p.trim());
  const usage: UsageItem[] = [];

  if (parts[0]) {
    usage.push({ website: parts[0] });
  }
  if (parts[1]) {
    usage.push({ "mobile app": parts[1] });
  }
  if (parts[2]) {
    usage.push({ "facebook application": parts[2] });
  }

  return { usage };
}

/**
 * Parse english preference field
 * Format: "1" or "0"
 * - "1" = American English
 * - "0" = British English
 *
 * Example: "1"
 */
export function parseEnglishPreference(raw: string | null): ParsedEnglishPreference {
  const value = raw?.trim();
  if (value === '0') {
    return { "english preference": "British English" };
  }
  // Default to American English for any other value including "1" or null
  return { "english preference": "American English" };
}

/**
 * Parse description field
 * Format: "confirmation_use_case*description"
 * - confirmation and use_case separated by _ (underscore)
 * - use_case and description separated by * (asterisk)
 *
 * Example: "yes_management lab*just kidding brother"
 */
export function parseDescription(raw: string | null): ParsedDescription {
  if (!raw || !raw.trim()) {
    return { "use and description": [] };
  }

  const trimmed = raw.trim();
  const [mainPart, descriptionPart] = trimmed.includes('*')
    ? trimmed.split('*', 2)
    : [trimmed, ''];

  const [confirmation, useCase] = mainPart.split('_', 2).map(p => p.trim());
  const description = descriptionPart.trim();

  return {
    "use and description": [{
      confirmation: confirmation || '',
      use_case: useCase || '',
      description
    }]
  };
}