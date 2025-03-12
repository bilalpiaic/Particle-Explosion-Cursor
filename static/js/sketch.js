let particles = [];
const MAX_PARTICLES = 1000; // Limit particles for performance

function setup() {
    // Create canvas inside container
    const canvas = createCanvas(windowWidth, windowHeight);
    canvas.parent('canvas-container');
    
    // Set initial background
    background(0);
}

function draw() {
    // Smooth fade effect
    background(0, 25);
    
    // Add new particles on mouse movement
    if (mouseIsPressed || frameCount % 2 === 0) {
        if (particles.length < MAX_PARTICLES) {
            particles.push(new Particle(mouseX, mouseY));
        }
    }
    
    // Update and display particles
    for (let i = particles.length - 1; i >= 0; i--) {
        const particle = particles[i];
        particle.update();
        particle.show();
        
        // Remove dead particles
        if (particle.isDead()) {
            particles.splice(i, 1);
        }
    }
}

function windowResized() {
    // Handle window resizing
    resizeCanvas(windowWidth, windowHeight);
    background(0);
}

// Optimize for mobile
function touchMoved() {
    // Prevent default touch behavior
    return false;
}
