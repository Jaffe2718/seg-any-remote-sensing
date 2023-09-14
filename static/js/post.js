// this is an example of a POST request using fetch
// TODO: delete this file if you don't need it

let url = document.URL;
window.alert(url);
let data = '{"msg": "Hello World!"}';

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
})
.then(response => response.json())
.then(data => console.log(data))
.catch((error) => console.error('Error:', error));