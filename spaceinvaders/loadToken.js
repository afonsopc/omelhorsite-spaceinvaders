const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');

console.log(`Setting token to ${token}`)

window.token = token;