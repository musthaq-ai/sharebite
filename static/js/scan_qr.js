let html5QrCode;

function onScanSuccess(decodedText) {

    html5QrCode.stop();

    fetch("/donor/verify-ngo", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            qr: decodedText

        })

    })

    .then(response => response.json())

    .then(data => {

        if(data.success){

            Swal.fire({

                icon: "success",

                title: "Food Handover Completed",

                text: data.message,

                confirmButtonColor: "#16a34a"

            }).then(()=>{

                window.location.href="/donor/my-donations";

            });

        }

        else{

            Swal.fire({

                icon:"error",

                title:"Verification Failed",

                text:data.message

            });

        }

    });

}

function onScanFailure(error) {

    // Ignore scan errors

}

async function startScanner() {

    html5QrCode = new Html5Qrcode("reader");

    try {

        // Mobile -> Rear Camera

        await html5QrCode.start(

            {

                facingMode: "environment"

            },

            {

                fps: 10,

                qrbox: {

                    width: 250,

                    height: 250

                }

            },

            onScanSuccess,

            onScanFailure

        );

    }

    catch {

        // Desktop fallback

        const cameras = await Html5Qrcode.getCameras();

        if (cameras.length > 0) {

            await html5QrCode.start(

                cameras[0].id,

                {

                    fps: 10,

                    qrbox: {

                        width: 250,

                        height: 250

                    }

                },

                onScanSuccess,

                onScanFailure

            );

        }

    }

}

window.addEventListener("load", startScanner);