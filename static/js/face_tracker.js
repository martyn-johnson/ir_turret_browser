let trackingEnabled = false;
let autoFireEnabled = false;
let calibrating = false;
let targetX = 320, targetY = 180;

const img = document.getElementById('video-feed');
const canvas = document.getElementById('canvas-overlay');
const ctx = canvas.getContext('2d');

async function loadModelAndStart() {
    const model = await blazeface.load();

    async function detectLoop() {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        const input = tf.browser.fromPixels(canvas);
        const predictions = await model.estimateFaces(input, false);
        input.dispose();

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = "lime";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(targetX - 10, targetY);
        ctx.lineTo(targetX + 10, targetY);
        ctx.moveTo(targetX, targetY - 10);
        ctx.lineTo(targetX, targetY + 10);
        ctx.stroke();

        if (predictions.length > 0 && trackingEnabled) {
            const face = predictions[0];
            const x = (face.topLeft[0] + face.bottomRight[0]) / 2;
            const y = (face.topLeft[1] + face.bottomRight[1]) / 2;

            ctx.beginPath();
            ctx.rect(face.topLeft[0], face.topLeft[1], 
                     face.bottomRight[0] - face.topLeft[0], 
                     face.bottomRight[1] - face.topLeft[1]);
            ctx.stroke();

            const offsetX = Math.round(x - targetX);
            const offsetY = Math.round(y - targetY);

            if (Math.abs(offsetX) > 10) {
                sendCommand("X" + offsetX);
            }
            if (Math.abs(offsetY) > 10) {
                sendCommand("Y" + offsetY);
            }

            if (autoFireEnabled && Math.abs(offsetX) < 15 && Math.abs(offsetY) < 15) {
                sendCommand("FIRE");
                await new Promise(r => setTimeout(r, 5000)); // wait 5s
            }
        }

        requestAnimationFrame(detectLoop);
    }

    detectLoop();
}

function sendCommand(cmd) {
    fetch('/command/' + cmd)
        .then(res => res.json())
        .then(data => console.log("[CMD]", data.command));
}

function toggleTracking() {
    trackingEnabled = !trackingEnabled;
}

function toggleAutoFire() {
    autoFireEnabled = !autoFireEnabled;
}

function startCalibration() {
    calibrating = true;
    canvas.addEventListener('click', function calibrateOnce(e) {
        const rect = canvas.getBoundingClientRect();
        const x = Math.round(e.clientX - rect.left);
        const y = Math.round(e.clientY - rect.top);
        targetX = x;
        targetY = y;

        fetch('/calibrate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ x, y })
        }).then(() => console.log("Calibrated:", x, y));

        calibrating = false;
        canvas.removeEventListener('click', calibrateOnce);
    });
}

window.onload = loadModelAndStart;
