// Password visibility
function setupToggle(buttonId, inputId) {

    const button = document.getElementById(buttonId);
    const input = document.getElementById(inputId);

    if (!button || !input) return;

    button.addEventListener("click", function () {

        if (input.type === "password") {

            input.type = "text";
            button.innerHTML = '<i class="bi bi-eye-slash"></i>';

        } else {

            input.type = "password";
            button.innerHTML = '<i class="bi bi-eye"></i>';
        }
    });
}

setupToggle("togglePassword", "password");
setupToggle("toggleConfirmPassword", "confirm_password");

// Password strength
const password = document.getElementById("password");

if (password) {

    password.addEventListener("keyup", function () {

        const value = password.value;

        const bar = document.getElementById("passwordStrengthBar");
        const text = document.getElementById("passwordStrengthText");

        let score = 0;

        if (value.length >= 8) score++;
        if (/[A-Z]/.test(value)) score++;
        if (/[0-9]/.test(value)) score++;
        if (/[^A-Za-z0-9]/.test(value)) score++;

        switch (score) {

            case 0:
            case 1:
                bar.style.width = "25%";
                bar.className = "progress-bar bg-danger";
                text.innerHTML = "Weak Password";
                break;

            case 2:
                bar.style.width = "50%";
                bar.className = "progress-bar bg-warning";
                text.innerHTML = "Medium Password";
                break;

            case 3:
                bar.style.width = "75%";
                bar.className = "progress-bar bg-info";
                text.innerHTML = "Good Password";
                break;

            case 4:
                bar.style.width = "100%";
                bar.className = "progress-bar bg-success";
                text.innerHTML = "Strong Password";
                break;
        }
    });
}

// Password match
const confirmPassword = document.getElementById("confirm_password");

if (confirmPassword && password) {

    confirmPassword.addEventListener("keyup", function () {

        const msg = document.getElementById("passwordMatchMessage");

        if (confirmPassword.value === "") {

            msg.innerHTML = "";
            return;
        }

        if (password.value === confirmPassword.value) {

            msg.innerHTML = "✔ Passwords match";
            msg.className = "text-success";

        } else {

            msg.innerHTML = "✖ Passwords do not match";
            msg.className = "text-danger";
        }
    });
}
function nextStep() {

    const step1 = document.getElementById("step1");

    const inputs = step1.querySelectorAll("input");

    for (const input of inputs) {

        if (!input.checkValidity()) {

            input.reportValidity();

            return;
        }

    }

    if (document.getElementById("password").value !==
        document.getElementById("confirm_password").value) {

        Swal.fire({
            icon: "warning",
            title: "Passwords do not match"
        });

        return;
    }

    document.getElementById("step1").style.display = "none";
    document.getElementById("step2").style.display = "block";

    document.getElementById("stepIndicator1").classList.add("completed");
    document.getElementById("stepIndicator2").classList.add("active");
}
function validateStep2() {

    const address = document.getElementById("address1").value.trim();

    const district = document.getElementById("district").value;

    const state = document.getElementById("state").value;

    const terms = document.getElementById("terms").checked;

    if (address === "") {

        Swal.fire({
            icon: "warning",
            title: "Address Required",
            text: "Please enter Address Line 1.",
            confirmButtonColor: "#198754"
        });

        return;
    }

    if (district === "") {

        Swal.fire({
            icon: "warning",
            title: "District Required",
            text: "Please select your district.",
            confirmButtonColor: "#198754"
        });

        return;
    }

    if (state === "") {

        Swal.fire({
            icon: "warning",
            title: "State Required",
            text: "Please select your state.",
            confirmButtonColor: "#198754"
        });

        return;
    }

    if (!terms) {

        Swal.fire({
            icon: "warning",
            title: "Terms & Conditions",
            text: "Please accept the Terms & Conditions to continue.",
            confirmButtonColor: "#198754"
        });

        return;
    }

    // Everything is valid
    document.getElementById("donorRegisterForm").submit();

}
function previousStep() {

    document.getElementById("step2").style.display = "none";
    document.getElementById("step1").style.display = "block";

    document.getElementById("stepIndicator1").classList.remove("completed");
    document.getElementById("stepIndicator2").classList.remove("active");
}