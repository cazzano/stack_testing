import { parseSellOnThirdParties, parseAIServices, parseOnlinePayments } from './disclosure_of_info';
import { parseUsage, parseEnglishPreference, parseDescription } from './policy_uses';
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

// Get input from args or prompt
async function getInput(prompt: string, args: string[], argIndex: number): Promise<string> {
  if (args.length > argIndex) {
    return args[argIndex];
  }
  return await question(prompt);
}

// Parse Third-Party Services
async function parseThirdParty(args: string[]) {
  const input = await getInput('Enter your third-party services string: ', args, 2);
  console.log('\nParsing...\n');
  const result = parseSellOnThirdParties(input);
  console.log('=== PARSED RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  console.log('\n');
}

// Parse AI Services
async function parseAI(args: string[]) {
  const input = await getInput('Enter your AI services string: ', args, 2);
  console.log('\nParsing...\n');
  const result = parseAIServices(input);
  console.log('=== PARSED RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  console.log('\n');
}

// Parse Online Payments
async function parsePayments(args: string[]) {
  const input = await getInput('Enter your online payments string: ', args, 2);
  console.log('\nParsing...\n');
  const result = parseOnlinePayments(input);
  console.log('=== PARSED RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  console.log('\n');
}

// Parse Usage
async function parseUsageField(args: string[]) {
  const input = await getInput('Enter your usage string: ', args, 2);
  console.log('\nParsing...\n');
  const result = parseUsage(input);
  console.log('=== PARSED RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  console.log('\n');
}

// Parse English Preference
async function parseEnglish(args: string[]) {
  const input = await getInput('Enter your english preference (1 for American, 0 for British): ', args, 2);
  console.log('\nParsing...\n');
  const result = parseEnglishPreference(input);
  console.log('=== PARSED RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  console.log('\n');
}

// Parse Description
async function parseDescriptionField(args: string[]) {
  const input = await getInput('Enter your description string: ', args, 2);
  console.log('\nParsing...\n');
  const result = parseDescription(input);
  console.log('=== PARSED RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  console.log('\n');
}

// Main program loop with CLI argument support
async function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    console.log('Usage:');
    console.log('  ts-node main.ts disclosure --third_party [input_string]');
    console.log('  ts-node main.ts disclosure --ai [input_string]');
    console.log('  ts-node main.ts disclosure --payments [input_string]');
    console.log('  ts-node main.ts uses --usage [input_string]');
    console.log('  ts-node main.ts uses --english [input_string]');
    console.log('  ts-node main.ts uses --description [input_string]');
    rl.close();
    return;
  }

  const [module, option] = args;

  switch (module) {
    case 'disclosure':
      switch (option) {
        case '--third_party':
          await parseThirdParty(args);
          break;
        case '--ai':
          await parseAI(args);
          break;
        case '--payments':
          await parsePayments(args);
          break;
        default:
          console.log('Invalid disclosure option. Use --third_party, --ai, or --payments');
      }
      break;

    case 'uses':
      switch (option) {
        case '--usage':
          await parseUsageField(args);
          break;
        case '--english':
          await parseEnglish(args);
          break;
        case '--description':
          await parseDescriptionField(args);
          break;
        default:
          console.log('Invalid uses option. Use --usage, --english, or --description');
      }
      break;

    default:
      console.log('Invalid module. Use "disclosure" or "uses"');
  }

  rl.close();
}

// Run the program
main().catch((error) => {
  console.error('Error:', error);
  rl.close();
  process.exit(1);
});