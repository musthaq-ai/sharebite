const openCamera = document.getElementById("openCamera");

if (openCamera) {

    const camera = document.getElementById("camera");
    const cameraContainer = document.getElementById("cameraContainer");
    const captureBtn = document.getElementById("captureBtn");
    const retakeBtn = document.getElementById("retakeBtn");
    const canvas = document.getElementById("canvas");
    const previewImage = document.getElementById("previewImage");
    const imageInput = document.getElementById("imageInput");

    let stream = null;

    // Open Camera
    openCamera.addEventListener("click", async () => {

        try {

            stream = await navigator.mediaDevices.getUserMedia({
                video: true
            });

            camera.srcObject = stream;

            cameraContainer.style.display = "block";

        } catch (err) {

            alert("Unable to access camera.");

            console.error(err);

        }

    });

    // Capture Photo
    captureBtn.addEventListener("click", () => {

        canvas.width = camera.videoWidth;
        canvas.height = camera.videoHeight;

        const ctx = canvas.getContext("2d");

        ctx.drawImage(camera, 0, 0);

        canvas.toBlob(function(blob){

            const file = new File(
                [blob],
                "captured_food.png",
                {
                    type:"image/png"
                }
            );

            const dt = new DataTransfer();

            dt.items.add(file);

            imageInput.files = dt.files;

            previewImage.src = URL.createObjectURL(file);

        });

        if(stream){

            stream.getTracks().forEach(track => track.stop());

        }

        camera.style.display = "none";

        captureBtn.style.display = "none";

        retakeBtn.style.display = "block";

    });

    // Retake
    retakeBtn.addEventListener("click", async () => {

        stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        camera.srcObject = stream;

        camera.style.display = "block";

        captureBtn.style.display = "block";

        retakeBtn.style.display = "none";

    });

    // Upload Preview
    imageInput.addEventListener("change", function(){

        if(this.files.length){

            previewImage.src = URL.createObjectURL(this.files[0]);

        }

    });

}