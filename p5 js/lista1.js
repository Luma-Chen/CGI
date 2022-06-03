//Este trabalho foi construído utilizando o programa p5.js

const FRAME_RATE = 30;
const GRID_ROWS = 3;
const GRID_COLS = 3;
const WINDOW = 300;
const colors = [[255, 0, 0], [0, 255, 0], [0, 0, 40], [5, 60, 80], [50, 170, 190], [200, 4, 255], [0, 0, 255], [59, 255, 210], [77, 35, 155]];

const MIN_EDGES = 3;
const MAX_EDGES = 12;
let snowflakes = [];
let currentEdges;
const moonTrailVectorsHist = [[], []];
let moonTrailController = [0, 0];
 
function drawGrid(colors) {
  let count = 0;
  
  for (let i = 0; i < GRID_COLS; i++) {
    const yCord = (i * height) / GRID_COLS; 
    for (let j = 0; j < GRID_ROWS; j++) {
      const xCord = (j * width) / GRID_ROWS;
      const topLeft = { x: xCord, y: yCord };
 
      fill(colors[count]);
      count++;
      rect(topLeft.x, topLeft.y, width, height);
    }
  }
}
 
function setCentralized(xQuadrant, yQuadrant) {
  const xCord = (width * (1 / GRID_COLS)) / 2 + WINDOW * (yQuadrant - 1);
  const yCord = width / GRID_ROWS / 2 + WINDOW * (xQuadrant - 1);
 
  return { x: xCord, y: yCord };
}
 
function shouldFrameChange(changes, intervalOnSecs) {
  if (frameCount % (FRAME_RATE * intervalOnSecs) === 0) {
    return true;
  }
  return false;
}

/* ----------- A) ------------ */
 
function getEdgesQnt(changesQnt, intervalOnSecs) {
  if (!currentEdges) {
    currentEdges = MIN_EDGES;
    return currentEdges;
  }
 
  if (currentEdges === MAX_EDGES + 1) {
    currentEdges = MIN_EDGES;
    return currentEdges;
  }
 
  if (shouldFrameChange(changesQnt, intervalOnSecs)) {
    currentEdges++;
  }
  return currentEdges;
}

function drawPolygons(radius, changesQnt, intervalOnSecs) {
  const n = getEdgesQnt(changesQnt, intervalOnSecs);
  const a = -TWO_PI/n;
 
  noFill();
  beginShape();
 
  for (let i = 0; i < n; ++i) {
    const y = radius * sin(i * a);
    const x = radius * cos(i * a);
    vertex(x, y);
  }
  endShape(CLOSE);
}
 
/* ----------- B) ------------ */

class KochLine {
  constructor(a,b) {
    this.start = a.copy();
    this.end = b.copy();
  }

  display() {
    stroke(255);
    line(this.start.x, this.start.y, this.end.x, this.end.y);
  }

  kochA() {
    return this.start.copy();
  }

  // This is easy, just 1/3 of the way
  kochB() {
    let v = p5.Vector.sub(this.end, this.start);
    v.div(3);
    v.add(this.start);
    return v;
  }

  kochC() {
    let a = this.start.copy(); // Start at the beginning
    let v = p5.Vector.sub(this.end, this.start);
    v.div(3);
    a.add(v);  // Move to point B
    v.rotate(-PI/3); // Rotate 60 degrees
    a.add(v);  // Move to point C
    return a;
  }

  // Easy, just 2/3 of the way
  kochD() {
    let v = p5.Vector.sub(this.end, this.start);
    v.mult(2/3.0);
    v.add(this.start);
    return v;
  }

  kochE() {
    return this.end.copy();
  }
}

class KochFractal {
  constructor() {
    this.start = createVector(0,height-20);   // A p5.Vector for the start
    this.end = createVector(width,height-20); // A p5.Vector for the end
    this.lines = [];                         // An array to keep track of all the lines
    this.count = 0;
    this.restart();
  }

  nextLevel() {
    this.lines = this.iterate(this.lines);
    this.count++;
  }

  restart() {
    this.count = 0;      // Reset count
    this.lines = [];  // Empty the array list
    this.lines.push(new KochLine(this.start,this.end));  // Add the initial line (from one end p5.Vector to the other)
  }

  getCount() {
    return this.count;
  }

  // This is easy, just draw all the lines
  render() {
    for(let i = 0; i < this.lines.length; i++) {
      this.lines[i].display();
    }
  }

  iterate(before) {
    let now = [];    // Create emtpy list
    for(let i = 0; i < this.lines.length; i++) {
      let l = this.lines[i];
      // Calculate 5 koch p5.Vectors (done for us by the line object)
      let a = l.kochA();
      let b = l.kochB();
      let c = l.kochC();
      let d = l.kochD();
      let e = l.kochE();
      // Make line segments between all the p5.Vectors and add them
      now.push(new KochLine(a,b));
      now.push(new KochLine(b,c));
      now.push(new KochLine(c,d));
      now.push(new KochLine(d,e));
    }
    return now;
  }
}
 
/* ----------- C) ----------- */
function drawSolarSys({ sun, earth, moon }, distanceToSunCenter) 
{
  fill(sun.color);
  circle(0, 0, sun.diameter);
  rotate(earth.rotation);
  fill(earth.color);
  circle(distanceToSunCenter, 0, earth.diameter);
  translate(distanceToSunCenter, 0);
  rotate(moon.rotation);
  fill(moon.color);
  circle(30, 0, moon.diameter);
}
 
/* ----------- D) ----------- */
function moonTrace(bigLapSeconds, littleLapSeconds, secondsToReset, i) 
{
  if (shouldMoonTrailRestart(secondsToReset, i)) 
  {
    moonTrailVectorsHist[i].length = 0;
  }
 
  const x =
    30 * cos(frameCount / littleLapSeconds / TWO_PI) +
    75 * cos(frameCount / bigLapSeconds / TWO_PI);
  const y =
    30 * sin(frameCount / littleLapSeconds / TWO_PI) +
    75 * sin(frameCount / bigLapSeconds / TWO_PI);
 
  const v = createVector(x, y);
  moonTrailVectorsHist[i].push(v);
  fill(0, 0, 0);
 
  for (
    let j = 0;
    j < moonTrailVectorsHist[i].length;
    j++
  ) {
    circle(
      moonTrailVectorsHist[i][j].x,
      moonTrailVectorsHist[i][j].y, 10
    );
  }
}
 
function shouldMoonTrailRestart(secondsToReset, i) {
  if (moonTrailController[i] === secondsToReset) {
    moonTrailController[i] = 0;
    return true;
  }
  if (frameCount % FRAME_RATE === 0) {
    moonTrailController[i]++;
  }
  return false;
}
 
let u = 0;
/* ----------- F) ----------- */
function framesBouncer(bounceLimit) {
  return frameCount % bounceLimit;
}
 
function drawButterfly(xScale, yScale, frameBounceLimit) {
  function x(u) {
    return cos(u) * (exp(cos(u)) - 2 * cos(4 * u) - pow(sin(u / 12), 5));
  }
 
  function y(u) {
    return sin(u) * (exp(cos(u)) - 2 * cos(4 * u) - pow(sin(u / 12), 5));
  }
 
  stroke(0, 0, 0);
  noFill();
  beginShape();
  for (let i = 0; i < 100; ++i) 
  {
    const xParam = (framesBouncer(frameBounceLimit) * i) / 1000;
    const yParam = (framesBouncer(frameBounceLimit) * i) / 1000;
 
    vertex(x(xParam) * xScale, y(yParam) * yScale);
  }
  endShape();
}

/*---------- H) -------------*/

function drawStar() 
{
  rotate(frameCount / 30.0);
  star(0, 0, 6, 80, 4);
}

function star(x, y, radius1, radius2, npoints) {
  let angle = TWO_PI / npoints;
  let halfAngle = angle / 2.0;
  fill([255,255,0]);
  beginShape();
  for (let a = 0; a < TWO_PI; a += angle) {
    let sx = x + cos(a) * radius2;
    let sy = y + sin(a) * radius2;
    vertex(sx, sy);
    sx = x + cos(a + halfAngle) * radius1;
    sy = y + sin(a + halfAngle) * radius1;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}

function snowflake() 
{  
  this.posX = 0;
  this.posY = random(-80, -80);
  this.initialangle = random(0, 2 * PI);
  this.size = random(2, 5);

  this.radius = sqrt(random(pow(width / 2, 2)));

  this.update = function(time) {
    let w = 0.6; 
    let angle = w * time + this.initialangle;
    this.posX = width/3 + this.radius * sin(angle);

    this.posY += pow(this.size, 0.5);
    if (this.posY > height) {
      let index = snowflakes.indexOf(this);
      snowflakes.splice(index, 1);
    }
  };
  this.display = function() {
    ellipse(this.posX, this.posY, this.size);
  };
}

function drawSnow() 
{
  let t = frameCount / 30; // update time
  fill(240);
  for (let i = 0; i < random(5); i++) {
    snowflakes.push(new snowflake()); 
  }

  for (let flake of snowflakes) {
    flake.update(t); 
    flake.display(); 
  }
}

function setup() {
  createCanvas(900, 900);
  frameRate(FRAME_RATE);
  angleMode(RADIANS);
}
 
function draw() {
  /* Questão 1 */
  
  drawGrid(colors);
  
  /* A) */
  
  push();
  const polygons = setCentralized(1, 1);
  translate(polygons.x, polygons.y);
  const radius = WINDOW * 0.4;
  const changesQnt = 9;
  const intervalOnSecs = 2;
  drawPolygons(radius, changesQnt, intervalOnSecs);
  pop();
  
  /* B) */
  
  push();
  const koch = setCentralized(1, 2);
  translate(koch.x, koch.y);
  k = new KochFractal();
  k.render();
  k.nextLevel();
  if (k.getCount() > 5) {
    k.restart();
  }
  pop();
 
  /* C) */
  
  push();
  const solarSys = setCentralized(1, 3);
  const solarSysElements = {
    sun: { color: [252, 212, 64], diameter: 75 },
    earth: { color: [107,147,214], diameter: 20, rotation: frameCount / 20 / TWO_PI },
    moon: { color: [255, 255, 255], diameter: 10, rotation: frameCount / 5 / TWO_PI },
  };
  distanceToSunCenter = 100;
  translate(solarSys.x, solarSys.y);
  drawSolarSys(solarSysElements, distanceToSunCenter);
  pop();
 
  /* D) */
  
  push();
  const moonTrailCenter = setCentralized(2, 1);
  translate(moonTrailCenter.x, moonTrailCenter.y);
  const bigLapSeconds = 20;
  const littleLapSeconds = 5;
  moonTrace(bigLapSeconds, littleLapSeconds, 27, 0);
  pop();
 
  /* E) */
  
  push();
  moonTraceII = setCentralized(2, 2);
  translate(moonTraceII.x, moonTraceII.y);
  moonTrace(10, 2, 14, 1);
  pop();
 
  /* F) */
  
  push();
  const fCenter = setCentralized(2, 3);
  translate(fCenter.x, fCenter.y);
  drawButterfly(30, 30, 70);
  pop();
  
  /* H)  */
  
  push();
  const star= setCentralized(3,2);
  translate(star.x, star.y);
  drawStar();
  pop();
  
  push();
  const snowFlake= setCentralized(3,3);
  translate(snowFlake.x, snowFlake.y);
  drawSnow()
  pop();
}