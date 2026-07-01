const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'index.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf8');

const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let scripts = [];
while ((match = scriptRegex.exec(htmlContent)) !== null) {
    scripts.push(match[1]);
}

const mainJs = scripts[scripts.length - 1];

fs.writeFileSync(path.join(__dirname, 'temp_check.js'), mainJs, 'utf8');
console.log('Main JS written to temp_check.js. Running syntax check...');
