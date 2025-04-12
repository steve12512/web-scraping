const fs = require('fs');

let html = fs.readFileSync('response_content.txt', 'utf-8',);

const pattern = /let\s+COMPENSATION_LIST\s*=\s*(\[\s*\{[\s\S]*?\}\s*(?:\,\s*\{[\s\S]*?\}\s*)*\])/;
const match = html.match(pattern);


if (match) {
    const json_like = match[1];
    console.log('true')

} else {
    console.log('no')
}