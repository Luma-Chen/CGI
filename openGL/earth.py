from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import png as png
from math import *

ESCAPE = b'\033'

# Number of the glut window.
window = 0

# Rotations for cube. 
xrot = yrot = zrot = 0.0
dx = 0.1
dy = 0
dz = 0



# texture = []

def LoadTextures():
    global texture
    texture = [ glGenTextures(1) ]

    ################################################################################
    glBindTexture(GL_TEXTURE_2D, texture[0])
    reader = png.Reader(filename='mapa.png')
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
#    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    ################################################################################


def InitGL(Width, Height):             
    LoadTextures()
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)               
    glEnable(GL_DEPTH_TEST)            
    glShadeModel(GL_SMOOTH)            
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0,0,-5)

def ReSizeGLScene(Width, Height):
    if Height == 0:                        
        Height = 1
    glViewport(0, 0, Width, Height)      
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

phi0 = 0
phin = 2*pi

theta0 = -pi/2
thetan = pi/2

n = 50

dphi = (phin - phi0)/n
dtheta = (thetan - theta0)/n


def esfera():
    # glDisable(GL_TEXTURE_2D)
    glRotatef(1,1,0,0)
    raio = 1

    phi = phi0
    for i in range(0,n+1):
        glBegin(GL_TRIANGLE_STRIP)
        theta = theta0
        # theta = (i*pi/n) - pi/2
        for j in range(0,n+1):
            # phi = (j*2*pi)/n
            x = raio*cos(theta)*cos(phi)
            y = raio*sin(theta)
            z = raio*cos(theta)*sin(phi)

            x_2 = raio*cos(theta)*cos(phi+dphi)
            y_2 = raio*sin(theta)
            z_2 = raio*cos(theta)*sin(phi+dphi)

            glTexCoord2f(i/(n-1),j/(n-1))
            glVertex3f(x,y,z)
            glTexCoord2f((i+1)/(n-1),j/(n-1))
            glVertex3f(x_2,y_2,z_2)

            theta += dtheta
        glEnd()
        phi += dphi
    
    # glEnable(GL_TEXTURE_2D)


def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    esfera()
    glutSwapBuffers()
 


def DrawGLScene2():
    global xrot, yrot, zrot, texture

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()                   
    glClearColor(0.5,0.5,0.5,1.0)            
    glTranslatef(0.0,0.0,-5.0)
    glRotatef(xrot,1.0,0.0,0.0)          
    glRotatef(yrot,0.0,1.0,0.0)           
    glRotatef(zrot,0.0,0.0,1.0) 
    
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glBegin(GL_QUADS)              
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    
    glTexCoord2f(0.0, 1/2); glVertex3f( 1.0, -1.0,  1.0)   
    glTexCoord2f(1/3, 1/2); glVertex3f( 1.0,  1.0,  1.0)   
    glTexCoord2f(1/3, 0.0); glVertex3f(-1.0,  1.0,  1.0)  

    # Back Face
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)    
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)    
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)   
    
    # Top Face
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)   
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)    
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)    
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)   

    # Bottom Face       
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)   
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)   
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)   
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    
    
    # Right face
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)    
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)   
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)    
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)  
    
    # Left Face
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)  
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)   
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)   
    
    glEnd()                # Done Drawing The Cube
    
    xrot = xrot + 0.01                # X rotation
    yrot = yrot + 0.01                 # Y rotation
    zrot = zrot + 0.01                 # Z rotation

    glutSwapBuffers()


def keyPressed(tecla, x, y):
    global dx, dy, dz
    if tecla == ESCAPE:
        glutLeaveMainLoop()
    elif tecla == b'x' or tecla == b'X':
        dx = 1.0
        dy = 0
        dz = 0   
    elif tecla == b'y' or tecla == b'Y':
        dx = 0
        dy = 1.0
        dz = 0   
    elif tecla == b'z' or tecla == b'Z':
        dx = 0
        dy = 0
        dz = 1.0

def teclaEspecialPressionada(tecla, x, y):
    global xrot, yrot, zrot, dx, dy, dz
    if tecla == GLUT_KEY_LEFT:
        print ("ESQUERDA")
        xrot -= dx                # X rotation
        yrot -= dy                 # Y rotation
        zrot -= dz                     
    elif tecla == GLUT_KEY_RIGHT:
        print ("DIREITA")
        xrot += dx                # X rotation
        yrot += dy                 # Y rotation
        zrot += dz                     
    elif tecla == GLUT_KEY_UP:
        print ("CIMA")
    elif tecla == GLUT_KEY_DOWN:
        print ("BAIXO")

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)    
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Globo Terrestre Textura")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(teclaEspecialPressionada)
    InitGL(640, 480)
    glutMainLoop()

main()