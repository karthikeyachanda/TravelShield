// LOGIN FUNCTION
// LOGIN FUNCTION
async function login(){

    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    if(!email || !password) { alert("Please enter credentials"); return; }

    try {
        let response = await fetch("http://127.0.0.1:5000/login",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({ email:email, password:password })
        });

        if(response.status === 401){ alert("❌ Invalid email or password"); return; }
        
        let data = await response.json();
        if(data.user){
            localStorage.setItem("user_id", data.user.id);
            localStorage.setItem("user_email", data.user.email);
            localStorage.setItem("user_name", data.user.name);
            alert("✅ Login successful");
            window.location.href="dashboard.html";
        } else {
            alert("❌ Login failed: " + (data.message || "Unknown error"));
        }
    } catch(e) {
        alert("⚠️ Server error - Is the backend running?");
    }
}


// REGISTER FUNCTION
async function register(){

    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    if(!name || !email || !password){
        alert("⚠️ Please fill in all fields (Name, Email, and Password)!"); 
        return;
    }

    try {
        let response = await fetch("http://127.0.0.1:5000/register",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({
                name:name,
                email:email,
                password:password
            })
        });

        let data = await response.json();

        if (response.ok) {
            alert("✅ Registration Successful! Please login with your credentials.");
            window.location.href="login.html";
        } else {
            alert("❌ Registration Error: " + (data.message || "Email might already be registered."));
        }
    } catch(err) {
        alert("⚠️ Connection Error - Is your backend Flask server running?");
        console.error(err);
    }
}