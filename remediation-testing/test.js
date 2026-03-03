// test.js
// This file was created to match the '*.js' pattern for testing purposes.

// Example usage of the elliptic package and ECDSA signing
const elliptic = require('elliptic');
const EC = elliptic.ec;
const ec = new EC('secp256k1');

// Generate a key pair
const key = ec.genKeyPair();

// Example message
const msg = 'Hello, ECDSA!';

// Sign the message using ECDSA
const signature = key.sign(msg);

console.log('Signature:', signature); 