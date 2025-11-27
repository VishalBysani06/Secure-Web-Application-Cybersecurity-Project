// Create floating particles
function createParticles() {
    for (let i = 0; i < 25; i++) {
        let particle = document.createElement("div");
        particle.classList.add("cyber-particle");

        particle.style.left = Math.random() * window.innerWidth + "px";
        particle.style.animationDelay = Math.random() * 4 + "s";
        particle.style.animationDuration = (5 + Math.random() * 5) + "s";

        document.body.appendChild(particle);
    }
}

// Create animated grid lines
function createLines() {
    for (let i = 0; i < 8; i++) {
        let line = document.createElement("div");
        line.classList.add("cyber-line");

        line.style.top = Math.random() * window.innerHeight + "px";
        line.style.animationDelay = Math.random() * 4 + "s";

        document.body.appendChild(line);
    }
}

createParticles();
createLines();
