/**
 * Parser for Disclosure of Information API data
 * Handles sell_on_third_parties, ai_services, and online_payments fields
 */

export interface ParsedThirdPartyService {
  provider: string;
  service: string;
  sharePersonalData: boolean; // "I add personal data to the above"
  shareSensitiveData: boolean; // "I share personal data to the above"
}

export interface ParsedThirdPartyCategory {
  categoryName: string;
  services: ParsedThirdPartyService[];
}

export interface ParsedSellOnThirdParties {
  categories: ParsedThirdPartyCategory[];
}

export interface ParsedAIServices {
  functions: string[];
  platforms: string[];
  optOutMethods: string[];
}

export interface ParsedOnlinePayments {
  vendors: Array<{
    vendorName: string;
    privacyPolicyUrl: string;
  }>;
  additionalDetails: string | null;
}

/**
 * Parse sell_on_third_parties field
 * Format: "CategoryName#Provider$Service^Flag1^Flag2#Provider2$Service2^Flag1_NextCategory#Provider$Service^Flag1*Other#Provider$Service^Flag1"
 * - Categories are separated by _ (underscore)
 * - Within a category, services are separated by # (hash)
 * - Provider and service are separated by $ (dollar)
 * - Flags are separated by ^ (caret)
 * - "Other" category starts after * (asterisk)
 * 
 * Example: "Advertising, Direct Marketing, & Lead Generation#Amazon$Ads of ecommerce^I add personal data to the above^I share personal data to the above#Daraz$11.11 Sale^I add personal data to the above_AI Platforms#Anthropic$Claude Sonnet^I add personal data to the above\\^I share personal data to the above*Other#Ethical Hacking$Pentesting^I add personal data to the above\\n^I share personal data to the above"
 */
export function parseSellOnThirdParties(raw: string | null): ParsedSellOnThirdParties {
  if (!raw || !raw.trim()) {
    return { categories: [] };
  }

  const trimmed = raw.trim();
  const categories: ParsedThirdPartyCategory[] = [];

  // First, separate "Other" category if present (after *)
  const [mainContent, otherContent] = trimmed.includes('*')
    ? trimmed.split('*', 2)
    : [trimmed, ''];

  // Split main content by _ to get categories
  // Each category has format: CategoryName#Provider$Service^Flags#Provider2$Service2^Flags
  const categoryParts = mainContent.split('_');
  
  for (const categoryPart of categoryParts) {
    if (!categoryPart.trim()) continue;
    
    // Find category name (everything before first #)
    const hashIndex = categoryPart.indexOf('#');
    if (hashIndex === -1) continue;
    
    const categoryName = categoryPart.substring(0, hashIndex).trim();
    const servicesStr = categoryPart.substring(hashIndex + 1);
    
    const services: ParsedThirdPartyService[] = [];
    
    // Split services by # (each service is Provider$Service^Flags)
    const serviceParts = servicesStr.split('#');
    
    for (const servicePart of serviceParts) {
      if (!servicePart.trim()) continue;
      
      // Split by $ to get provider and service+flags
      const dollarIndex = servicePart.indexOf('$');
      if (dollarIndex === -1) continue;
      
      const provider = servicePart.substring(0, dollarIndex).trim();
      const serviceAndFlags = servicePart.substring(dollarIndex + 1);
      
      // Split by ^ to get service name and flags
      // Note: flags may contain escaped ^ characters (\\^)
      // First, handle escaped carets by temporarily replacing them
      const tempMarker = '___ESCAPED_CARET___';
      const normalized = serviceAndFlags.replace(/\\\\\^/g, tempMarker);
      
      // Split by ^ to separate service name from flags
      const parts = normalized.split('^');
      
      if (parts.length === 1) {
        // No flags, just service name
        services.push({
          provider,
          service: serviceAndFlags.replace(/\\n/g, ' ').trim(),
          sharePersonalData: false,
          shareSensitiveData: false
        });
        continue;
      }
      
      // First part is the service name, rest are flags
      const service = parts[0].replace(tempMarker, '\\^').replace(/\\n/g, ' ').trim();
      const flags = parts.slice(1).map(f => f.replace(tempMarker, '\\^').replace(/\\n/g, ' ').trim());
      
      // Check flags (handle escaped characters)
      const flagsStr = flags.join(' ').replace(/\\\\/g, '').toLowerCase();
      const sharePersonalData = flagsStr.includes('i add personal data');
      const shareSensitiveData = flagsStr.includes('i share personal data');
      
      services.push({
        provider,
        service,
        sharePersonalData,
        shareSensitiveData
      });
    }
    
    if (services.length > 0) {
      categories.push({ categoryName, services });
    }
  }

  // Handle "Other" category
  if (otherContent.trim()) {
    const otherCategory: ParsedThirdPartyCategory = {
      categoryName: 'Other',
      services: []
    };

    // Parse other content: "Other#Provider$Service^Flags" or just "Provider$Service^Flags"
    let otherServicesStr = otherContent;
    if (otherContent.startsWith('Other#')) {
      otherServicesStr = otherContent.substring(6); // Remove "Other#"
    }
    
    const serviceParts = otherServicesStr.split('#');
    for (const servicePart of serviceParts) {
      if (!servicePart.trim()) continue;
      
      const dollarIndex = servicePart.indexOf('$');
      if (dollarIndex === -1) continue;
      
      const provider = servicePart.substring(0, dollarIndex).trim();
      const serviceAndFlags = servicePart.substring(dollarIndex + 1);
      
      // Handle escaped carets
      const tempMarker = '___ESCAPED_CARET___';
      const normalized = serviceAndFlags.replace(/\\\\\^/g, tempMarker);
      
      // Split by ^ to separate service name from flags
      const parts = normalized.split('^');
      
      if (parts.length === 1) {
        otherCategory.services.push({
          provider,
          service: serviceAndFlags.replace(/\\n/g, ' ').trim(),
          sharePersonalData: false,
          shareSensitiveData: false
        });
        continue;
      }
      
      // First part is the service name, rest are flags
      const service = parts[0].replace(tempMarker, '\\^').replace(/\\n/g, ' ').trim();
      const flags = parts.slice(1).map(f => f.replace(tempMarker, '\\^').replace(/\\n/g, ' ').trim());
      
      const flagsStr = flags.join(' ').replace(/\\\\/g, '').toLowerCase();
      const sharePersonalData = flagsStr.includes('i add personal data');
      const shareSensitiveData = flagsStr.includes('i share personal data');
      
      otherCategory.services.push({
        provider,
        service,
        sharePersonalData,
        shareSensitiveData
      });
    }

    if (otherCategory.services.length > 0) {
      categories.push(otherCategory);
    }
  }

  return { categories };
}

/**
 * Parse ai_services field
 * Format: "Function1_Function2#Platform1_Platform2*OptOut1_OptOut2"
 * - After _: new function/platform/opt-out method
 * - After #: separator between functions and platforms
 * - After *: separator before opt-out methods
 */
export function parseAIServices(raw: string | null): ParsedAIServices {
  if (!raw || !raw.trim()) {
    return { functions: [], platforms: [], optOutMethods: [] };
  }

  const trimmed = raw.trim();
  
  // Split by * to separate opt-out methods
  const [mainContent, optOutContent] = trimmed.includes('*')
    ? trimmed.split('*', 2)
    : [trimmed, ''];

  // Split main content by # to separate functions and platforms
  const [functionsContent, platformsContent] = mainContent.includes('#')
    ? mainContent.split('#', 2)
    : [mainContent, ''];

  const functions = functionsContent
    .split('_')
    .map(f => f.trim())
    .filter(Boolean);

  const platforms = platformsContent
    .split('_')
    .map(p => p.trim())
    .filter(Boolean);

  const optOutMethods = optOutContent
    .split('_')
    .map(m => m.trim())
    .filter(Boolean);

  return { functions, platforms, optOutMethods };
}

/**
 * Parse online_payments field
 * Format: "Vendor1#URL1_Vendor2#URL2*AdditionalDetails"
 * - After #: privacy policy URL
 * - After _: new vendor separator
 * - After *: additional details separator
 */
export function parseOnlinePayments(raw: string | null): ParsedOnlinePayments {
  if (!raw || !raw.trim()) {
    return { vendors: [], additionalDetails: null };
  }

  const trimmed = raw.trim();
  
  // Split by * to separate additional details
  const [vendorsContent, additionalDetails] = trimmed.includes('*')
    ? trimmed.split('*', 2)
    : [trimmed, ''];

  const vendors: Array<{ vendorName: string; privacyPolicyUrl: string }> = [];
  
  // Split by _ to get individual vendors
  const vendorParts = vendorsContent.split('_');
  
  for (const vendorPart of vendorParts) {
    if (!vendorPart.trim()) continue;
    
    // Split by # to get vendor name and URL
    const [vendorName, ...urlParts] = vendorPart.split('#');
    const privacyPolicyUrl = urlParts.join('#').trim(); // Join in case URL contains #
    
    if (vendorName.trim() && privacyPolicyUrl) {
      vendors.push({
        vendorName: vendorName.trim(),
        privacyPolicyUrl
      });
    }
  }

  return {
    vendors,
    additionalDetails: additionalDetails.trim() || null
  };
}


