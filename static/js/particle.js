class Particle {
    constructor(x, y) {
        this.pos = createVector(x, y);
        this.vel = p5.Vector.random2D().mult(random(1, 3));
        this.size = random(5, 20);
        this.lifetime = 255;
        this.color = color(255, 255, 255, this.lifetime);
    }
    
    update() {
        // Update position based on velocity
        this.pos.add(this.vel);
        
        // Shrinking effect
        this.size *= 0.95;
        
        // Decrease lifetime
        this.lifetime -= 5;
        
        // Update color with new alpha
        this.color = color(255, 255, 255, this.lifetime);
    }
    
    show() {
        noStroke();
        fill(this.color);
        ellipse(this.pos.x, this.pos.y, this.size);
    }
    
    isDead() {
        return this.size < 1 || this.lifetime < 0;
    }
}
