let clicks = [];
let state = 0; // 0=waiting, 1=drawing first line, 2=fractal mode

function setup() {
  createCanvas(windowWidth, windowHeight);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

function mousePressed() {
  if (state === 0) {
    clicks[0] = createVector(mouseX, mouseY);
    state = 1;
  } else if (state === 1) {
    clicks[1] = createVector(mouseX, mouseY);
    state = 2;
  }
}

function draw() {
  background(255);
  stroke(0);
  strokeWeight(1.5);
  noFill();

  if (state === 0) {
    // do nothing
    return;
  }

  if (state === 1) {
    // draw line from first click to mouse
    line(clicks[0].x, clicks[0].y, mouseX, mouseY);
    return;
  }

  // state === 2: fractal mode
  // Base line: clicks[0] -> clicks[1]
  let base = p5.Vector.sub(clicks[1], clicks[0]);
  let baseLen = base.mag();
  let baseAngle = base.heading();

  // Current line: clicks[1] -> mouse
  let cur = createVector(mouseX - clicks[1].x, mouseY - clicks[1].y);
  let curLen = cur.mag();
  let curAngle = cur.heading();

  // Scale factor and angle offset between the two lines
  let scaleFactor = baseLen > 0 ? curLen / baseLen : 0;
  let angleOffset = curAngle - baseAngle;

  // Draw the base line
  line(clicks[0].x, clicks[0].y, clicks[1].x, clicks[1].y);

  // Recursively draw fractal lines
  let depth = 30;
  let px = clicks[1].x;
  let py = clicks[1].y;
  let angle = baseAngle;
  let len = baseLen;

  for (let i = 0; i < depth; i++) {
    angle += angleOffset;
    len *= scaleFactor;
    let nx = px + cos(angle) * len;
    let ny = py + sin(angle) * len;
    line(px, py, nx, ny);
    px = nx;
    py = ny;
  }
}
