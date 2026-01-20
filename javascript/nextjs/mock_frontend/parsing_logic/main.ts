import { parseSellOnThirdParties, parseAIServices, parseOnlinePayments } from './disclosure_of_info';
import * as readline from 'readline';

// Create readline interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Helper function to ask questions
function question(prompt: string): Promise<string> {
  return new Promise((resolve) => {
    rl.question(prompt, (answer) => {
      resolve(answer);
    });
  });
}

// Display menu and format guides
async function showMenu() {
  console.log('\n=== Disclosure of Information Parser ===\n');
  console.log('Choose what you want to parse:');
  console.log('1. Third-Party Services (sell_on_third_parties)');
  console.log('2. AI Services (ai_services)');
  console.log('3. Online Payments (online_payments)');
  console.log('4. Exit\n');
}

// Show format guide for Third-Party Services
function showThirdPartyFormat() {
  console.log('\n--- Third-Party Services Format Guide ---');
  console.log('Format: CategoryName#Provider$Service^Flag1^Flag2#Provider2$Service2_NextCategory#Provider$Service*Other#Provider$Service');
  console.log('\nDelimiters:');
  console.log('  _ (underscore) = separates categories');
  console.log('  # (hash) = separates services within a category');
  console.log('  $ (dollar) = separates provider from service');
  console.log('  ^ (caret) = separates flags');
  console.log('  * (asterisk) = starts "Other" category');
  console.log('\nFlags:');
  console.log('  "I add personal data to the above" = marks sharePersonalData as true');
  console.log('  "I share personal data to the above" = marks shareSensitiveData as true');
  console.log('\nExample:');
  console.log('Advertising#Amazon$Ads^I add personal data to the above^I share personal data to the above_AI Platforms#Anthropic$Claude*Other#TestProvider$TestService');
  console.log('---\n');
}

// Show format guide for AI Services
function showAIServicesFormat() {
  console.log('\n--- AI Services Format Guide ---');
  console.log('Format: Function1_Function2#Platform1_Platform2*OptOut1_OptOut2');
  console.log('\nDelimiters:');
  console.log('  _ (underscore) = separates functions/platforms/opt-out methods');
  console.log('  # (hash) = separates functions from platforms');
  console.log('  * (asterisk) = separates before opt-out methods');
  console.log('\nExample:');
  console.log('Content Generation_Code Assistance#ChatGPT_Claude_Gemini*Email opt-out_Account settings');
  console.log('---\n');
}

// Show format guide for Online Payments
function showOnlinePaymentsFormat() {
  console.log('\n--- Online Payments Format Guide ---');
  console.log('Format: Vendor1#URL1_Vendor2#URL2*AdditionalDetails');
  console.log('\nDelimiters:');
  console.log('  # (hash) = separates vendor name from privacy policy URL');
  console.log('  _ (underscore) = separates vendors');
  console.log('  * (asterisk) = separates before additional details');
  console.log('\nExample:');
  console.log('PayPal#https://paypal.com/privacy_Stripe#https://stripe.com/privacy*We use secure payment processing');
  console.log('---\n');
}

// Parse Third-Party Services
async function parseThirdParty() {
  showThirdPartyFormat();
  const input = await question('Enter your third-party services string: ');
  
  console.log('\nParsing...\n');
  const result = parseSellOnThirdParties(input);
  console.log('=== PARSED RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  console.log('\n');
}

// Parse AI Services
async function parseAI() {
  showAIServicesFormat();
  const input = await question('Enter your AI services string: ');
  
  console.log('\nParsing...\n');
  const result = parseAIServices(input);
  console.log('=== PARSED RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  console.log('\n');
}

// Parse Online Payments
async function parsePayments() {
  showOnlinePaymentsFormat();
  const input = await question('Enter your online payments string: ');
  
  console.log('\nParsing...\n');
  const result = parseOnlinePayments(input);
  console.log('=== PARSED RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  console.log('\n');
}

// Main program loop
async function main() {
  let running = true;
  
  while (running) {
    await showMenu();
    const choice = await question('Enter your choice (1-4): ');
    
    switch (choice.trim()) {
      case '1':
        await parseThirdParty();
        break;
      case '2':
        await parseAI();
        break;
      case '3':
        await parsePayments();
        break;
      case '4':
        console.log('\nGoodbye! 👋\n');
        running = false;
        break;
      default:
        console.log('\nInvalid choice. Please enter 1-4.\n');
    }
  }
  
  rl.close();
}

// Run the program
main().catch((error) => {
  console.error('Error:', error);
  rl.close();
  process.exit(1);
});
