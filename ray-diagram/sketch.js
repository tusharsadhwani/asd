function setup() {
  createCanvas(windowWidth, windowHeight);
  textSize(32);
  textFont("Times New Roman");
  strokeWeight(2);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

function draw() {
  background(255);
  translate(width / 2, height / 2);
  stroke(0);
  fill(0);
  ellipse(0, 0, 5);
  ellipse(width * 0.2, 0, 5);
  ellipse(width * 0.4, 0, 5);
  text("C", 0, 32);
  text("F", width * 0.2, 32);
  text("P", width * 0.41, 32);
  line(-width, 0, width * 0.4, 0);
  noFill();
  arc(0, 0, width * 0.8, width * 0.8, -0.5, 0.5, OPEN);

  const arrow_size = min(width, height) / 5;
  const head_size = arrow_size / 20;

  const translated_x = mouseX - width / 2;
  const translated_y = mouseY - height / 2;
  line(translated_x, 0, translated_x, -arrow_size);
  line(
    translated_x,
    -arrow_size,
    translated_x - head_size,
    head_size - arrow_size
  );
  line(
    translated_x,
    -arrow_size,
    translated_x + head_size,
    head_size - arrow_size
  );

  u = width * 0.4 - translated_x;
  f = width * 0.2;
  image_x = width * 0.4 - (u * f) / (u - f);
  m = (width * 0.4 - image_x) / (width * 0.4 - translated_x);
  image_y = m * arrow_size;
  stroke(0, 0, 255);
  line(image_x, 0, image_x, image_y);
  line(image_x, image_y, image_x - head_size * m, image_y - head_size * m);
  line(image_x, image_y, image_x + head_size * m, image_y - head_size * m);
}
