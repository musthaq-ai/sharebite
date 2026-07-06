document.addEventListener("DOMContentLoaded", function () {

    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm_password");

    const strengthBar = document.getElementById("passwordStrengthBar");
    const strengthText = document.getElementById("passwordStrengthText");

    const matchMessage = document.getElementById("passwordMatchMessage");

    const rules = {
        length: document.getElementById("rule-length"),
        upper: document.getElementById("rule-upper"),
        lower: document.getElementById("rule-lower"),
        number: document.getElementById("rule-number"),
        special: document.getElementById("rule-special")
    };

    password.addEventListener("input", function () {

        const value = password.value;

        let score = 0;

        if (value.length >= 8) {

            score++;
            rules.length.className = "d-block text-success";
            rules.length.innerHTML = "✅ Minimum 8 characters";

        } else {

            rules.length.className = "d-block text-danger";
            rules.length.innerHTML = "❌ Minimum 8 characters";

        }

        if (/[A-Z]/.test(value)) {

            score++;
            rules.upper.className = "d-block text-success";
            rules.upper.innerHTML = "✅ One uppercase letter";

        } else {

            rules.upper.className = "d-block text-danger";
            rules.upper.innerHTML = "❌ One uppercase letter";

        }

        if (/[a-z]/.test(value)) {

            score++;
            rules.lower.className = "d-block text-success";
            rules.lower.innerHTML = "✅ One lowercase letter";

        } else {

            rules.lower.className = "d-block text-danger";
            rules.lower.innerHTML = "❌ One lowercase letter";

        }

        if (/[0-9]/.test(value)) {

            score++;
            rules.number.className = "d-block text-success";
            rules.number.innerHTML = "✅ One number";

        } else {

            rules.number.className = "d-block text-danger";
            rules.number.innerHTML = "❌ One number";

        }

        if (/[^A-Za-z0-9]/.test(value)) {

            score++;
            rules.special.className = "d-block text-success";
            rules.special.innerHTML = "✅ One special character";

        } else {

            rules.special.className = "d-block text-danger";
            rules.special.innerHTML = "❌ One special character";

        }

        updateStrength(score);

    });

    confirmPassword.addEventListener("input", function () {

        if (confirmPassword.value === password.value) {

            matchMessage.innerHTML = "✅ Passwords match";
            matchMessage.className = "text-success";

        } else {

            matchMessage.innerHTML = "❌ Passwords do not match";
            matchMessage.className = "text-danger";

        }

    });

    function updateStrength(score) {

        switch(score){

            case 0:

                strengthBar.style.width="0%";
                strengthBar.className="progress-bar bg-danger";
                strengthText.innerHTML="Password Strength";

                break;

            case 1:

                strengthBar.style.width="20%";
                strengthBar.className="progress-bar bg-danger";
                strengthText.innerHTML="Very Weak";

                break;

            case 2:

                strengthBar.style.width="40%";
                strengthBar.className="progress-bar bg-warning";
                strengthText.innerHTML="Weak";

                break;

            case 3:

                strengthBar.style.width="60%";
                strengthBar.className="progress-bar bg-info";
                strengthText.innerHTML="Medium";

                break;

            case 4:

                strengthBar.style.width="80%";
                strengthBar.className="progress-bar bg-primary";
                strengthText.innerHTML="Strong";

                break;

            case 5:

                strengthBar.style.width="100%";
                strengthBar.className="progress-bar bg-success";
                strengthText.innerHTML="Very Strong";

                break;

        }

    }

});