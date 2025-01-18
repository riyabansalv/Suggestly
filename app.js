require('dotenv').config(); // Load variables from .env

const apiKey = process.env.API_KEY;

if (!apiKey) {
  console.error("API_KEY is missing! Check your .env file.");
  process.exit(1); // Exit if the API_KEY isn't set
}

// Your application logic here
console.log("Your API Key is:", apiKey);
