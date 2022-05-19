int width = 300;
int height= 300;
int cols= 3;
int rows= 3;

void setup() {
  size(900, 900);
}

void draw() { 
  int[][] colors= {{255, 0, 0}, {0, 255, 0}, {0, 0, 255}, {5, 60, 80}, {7, 20, 40}, {200, 4, 255}, {70, 100, 89}, {59, 255, 91}, {77, 35, 155}};
  int count= 0;
  for(int i= 0; i< rows; i++) {
    int x= i* width;
      
    for (int j= 0; j< cols; j++) {
      int y= j * width;
      rect (x, y, width, height);
      fill(colors[count][0], colors[count][1], colors[count][2]);
      count++;
    }
  }
}
