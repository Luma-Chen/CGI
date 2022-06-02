const FRAME_RATE = 30;
const GRID_ROWS = 3;
const GRID_COLS = 3;
const WINDOW = 300;
const colors = [[255, 0, 0], [0, 255, 0], [0, 0, 40], [5, 60, 80], [7, 170, 190], [200, 4, 255], [0, 0, 255], [59, 255, 210], [77, 35, 155]]; 
const MIN_EDGES = 3;
const MAX_EDGES = 12;

let currentEdges;
const moonTrailVectorsHist = [[], []];
let moonTrailController = 0;
 
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
 
function getGridCelCenter(xQuadrant, yQuadrant) {
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
 
function drawPoligon(radius, changesQnt, intervalOnSecs) {
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
 
// /* ----------- B) ----------- */

 
/* ----------- C) ----------- */
function drawSolarSystem({ sun, earth, moon }, distanceToSunCenter) {
  /* Sun */
  fill(sun.color);
  circle(0, 0, sun.diameter);
  /* Earth */
  rotate(earth.rotation);
  fill(earth.color);
  circle(distanceToSunCenter, 0, earth.diameter);
  translate(distanceToSunCenter, 0);
  /* Moon */
  rotate(moon.rotation);
  fill(moon.color);
  circle(30, 0, moon.diameter);
}
 
/* ----------- D) ----------- */
function drawMoonTrail(
  bigLapSeconds,
  littleLapSeconds,
  secondsToReset,
  moonTrailVectorsHistIndex
) {
  if (shouldMoonTrailRestart(secondsToReset)) {
    moonTrailVectorsHist[moonTrailVectorsHistIndex].length = 0;
  }
 
  const x =
    30 * cos(frameCount / littleLapSeconds / TWO_PI) +
    75 * cos(frameCount / bigLapSeconds / TWO_PI);
  const y =
    30 * sin(frameCount / littleLapSeconds / TWO_PI) +
    75 * sin(frameCount / bigLapSeconds / TWO_PI);
 
  const v = createVector(x, y);
  moonTrailVectorsHist[moonTrailVectorsHistIndex].push(v);
  fill(0, 0, 0);
 
  for (
    let i = 0;
    i < moonTrailVectorsHist[moonTrailVectorsHistIndex].length;
    ++i
  ) {
    circle(
      moonTrailVectorsHist[moonTrailVectorsHistIndex][i].x,
      moonTrailVectorsHist[moonTrailVectorsHistIndex][i].y,
      10
    );
  }
}
 
function shouldMoonTrailRestart(secondsToReset) {
  if (moonTrailController === secondsToReset) {
    moonTrailController = 0;
    return true;
  }
  if (frameCount % FRAME_RATE === 0) {
    moonTrailController++;
  }
  return false;
}
 
let u = 0;
/* ----------- F) ----------- */
function framesBouncer(bounceLimit) {
  return frameCount % bounceLimit;
}
 
function drawPFunction(xScale, yScale, frameBounceLimit) {
  function x(u) {
    return cos(u) * (exp(cos(u)) - 2 * cos(4 * u) - pow(sin(u / 12), 5));
  }
 
  function y(u) {
    return sin(u) * (exp(cos(u)) - 2 * cos(4 * u) - pow(sin(u / 12), 5));
  }
 
  stroke(0, 0, 0);
  noFill();
  beginShape();
  for (let i = 0; i < 100; ++i) {
    const xParam = (framesBouncer(frameBounceLimit) * i) / 1000;
    const yParam = (framesBouncer(frameBounceLimit) * i) / 1000;
 
    vertex(x(xParam) * xScale, y(yParam) * yScale);
  }
  endShape();
}
 
 
function setup() {
  createCanvas(900, 900);
  frameRate(FRAME_RATE);
  angleMode(RADIANS);
}
 
function draw() {
  /* questão 1 */
  
  drawGrid(colors);
  
  /* questão 1 a) */
  
  push();
  const circleCenter = getGridCelCenter(1, 1);
  translate(circleCenter.x, circleCenter.y);
  const radius = WINDOW * 0.4;
  const changesQnt = 9;
  const intervalOnSecs = 2;
  drawPoligon(radius, changesQnt, intervalOnSecs);
  pop();
  /* questão 1 b) */
  // push();
 
  /* questão 1 c) */
  push();
  const solarSystemCenter = getGridCelCenter(1, 3);
  const solarSystemObjects = {
    sun: { color: "yellow", diameter: 75 },
    earth: { color: "blue", diameter: 20, rotation: frameCount / 20 / TWO_PI },
    moon: { color: "white", diameter: 10, rotation: frameCount / 5 / TWO_PI },
  };
  distanceToSunCenter = 100;
  translate(solarSystemCenter.x, solarSystemCenter.y);
  drawSolarSystem(solarSystemObjects, distanceToSunCenter);
  pop();
 
  /* questão 1 d) */
  push();
  const moonTrailCenter = getGridCelCenter(2, 1);
  translate(moonTrailCenter.x, moonTrailCenter.y);
  const secondsToReset = 27;
  const bigLapSeconds = 20;
  const littleLapSeconds = 5;
  drawMoonTrail(bigLapSeconds, littleLapSeconds, secondsToReset, 0);
  pop();
 
  /* questão 1 e) */
  push();
  secondMoonTrailCenter = getGridCelCenter(2, 2);
  translate(secondMoonTrailCenter.x, secondMoonTrailCenter.y);
  drawMoonTrail(10, 2, secondsToReset, 1);
  pop();
 
  /* questão 1 f) */
  push();
  const fCenter = getGridCelCenter(2, 3);
  translate(fCenter.x, fCenter.y);
  drawPFunction(30, 30, 70);
  pop();
}
