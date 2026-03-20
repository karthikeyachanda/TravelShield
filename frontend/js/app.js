// LOGIN FUNCTION
async function login(){

let email = document.getElementById("email").value
let password = document.getElementById("password").value

let response = await fetch("http://127.0.0.1:5000/login",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
email:email,
password:password
})

})

let data = await response.json()

alert(data.message)

if(data.message === "Login successful"){
window.location.href="dashboard.html"
}

}


// REGISTER FUNCTION
async function register(){

let name = document.getElementById("name").value
let email = document.getElementById("email").value
let password = document.getElementById("password").value

let response = await fetch("http://127.0.0.1:5000/register",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
name:name,
email:email,
password:password
})

})

let data = await response.json()

alert(data.message)

if(data.message === "User registered successfully"){
window.location.href="login.html"
}

}