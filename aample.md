this is our database when user click the create button all the information should store in the database and the otp should come that email which user spiceifies give this updated code and alos update the index page and give otp.html file and connect the neccasary command and give updated code






<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>OTP Verification</title>

<style>
body {
    background: #0f0f1a;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    font-family: sans-serif;
    color: white;
}

.box {
    background: #1c1c2b;
    padding: 40px;
    border-radius: 15px;
    text-align: center;
}

input {
    padding: 12px;
    width: 200px;
    border-radius: 8px;
    border: none;
    margin-bottom: 15px;
}

button {
    padding: 10px 20px;
    background: #7a3cff;
    border: none;
    border-radius: 8px;
    color: white;
    cursor: pointer;
}
</style>
</head>

<body>

<div class="box">
    <h2>Enter OTP</h2>
    <input type="text" id="otp" placeholder="Enter OTP">
    <br>
    <button onclick="verifyOTP()">Verify</button>
    <p id="msg"></p>
</div>

<script>
async function verifyOTP() {
    let otp = document.getElementById("otp").value;

    let res = await fetch("/verify_otp", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({otp})
    });

    let data = await res.json();

    if (data.status === "success") {
        document.getElementById("msg").innerText = "Account Created ✅";
    } else {
        document.getElementById("msg").innerText = "Invalid OTP ❌";
    }
}
</script>

</body>
</html>