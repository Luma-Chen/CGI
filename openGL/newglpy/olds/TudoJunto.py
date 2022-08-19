from OpenGL.GL import *
import sys
import sdl2
import glm
import ctypes
import math

shader = {

    GL_VERTEX_SHADER: """
        #version 400

        layout (location=0) in vec3 position;
        layout (location=1) in vec3 color;
        uniform mat4 MVP;
        out vec3 colorToFragmentShader;

        void main(void) 
        {
            gl_Position = MVP * vec4(position,1.0);
            colorToFragmentShader = color;
        }
    """,

    GL_FRAGMENT_SHADER: """
        #version 400

        in vec3 colorToFragmentShader;
        out vec4 color;

        void main(void) 
        {
            color = vec4(colorToFragmentShader, 1.0f);
        }
    """
}

def preparaCubo():

    cubeVertex = [
        -1.0, -1.0,  1.0,
         1.0, -1.0,  1.0,
         1.0,  1.0,  1.0,
        -1.0,  1.0,  1.0,
        -1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0
    ]

    cubeColor = [
        1.0,  0.0,  0.0,
        1.0,  1.0,  0.0,
        0.0,  1.0,  0.0,
        0.0,  1.0,  1.0,
        0.0,  0.0,  1.0,
        1.0,  0.0,  1.0,
        1.0,  0.0,  0.5,
        0.5,  0.0,  0.5
    ]

    index = [
        0, 1, 2,
        2, 3, 0,
        1, 5, 6,
        6, 2, 1,
        3, 2, 6,
        6, 7, 3,
        4, 0, 3,
        3, 7, 4,
        5, 4, 7,
        7, 6, 5,
        4, 5, 1,
        1, 0, 4
    ]

    idVa = glGenVertexArrays(1)
    glBindVertexArray(idVa)
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    cubeVertexData = (GLfloat*len(cubeVertex))(*cubeVertex) 
    idVertexBuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, idVertexBuffer)
    glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(cubeVertexData), cubeVertexData, GL_STATIC_DRAW)
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))

    cubeColorData = (GLfloat*len(cubeColor))(*cubeColor)
    idColorBuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, idColorBuffer)
    glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(cubeColorData), cubeColorData, GL_STATIC_DRAW)
    glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))

    indexData = (GLuint*len(index))(*index)
    idIndex = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, idIndex);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, ctypes.sizeof(indexData), indexData, GL_STATIC_DRAW);
    return idVa

def desenhaCubo(idVa):
    glBindVertexArray(idVa)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, ctypes.c_void_p(0))

idVa = None
idProg = None
a=0

def desenha():
    global idVa, idProg, a
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    if idProg == None:
        idProg = createShaderProgram(shader)
        glUseProgram(idProg)
    if idVa == None:
        idVa = preparaCubo()

    mvpId = glGetUniformLocation(idProg,"MVP")    
    p = glm.perspective(glm.radians(45),WINDOW_WIDTH/WINDOW_HEIGHT,0.1,100)
    v = glm.lookAt(glm.vec3(0,0,20),glm.vec3(0,0,0),glm.vec3(0,1,0))
    
    #CUBO 1o quadrante
    m = glm.translate(glm.vec3(3,3,0)) * glm.rotate(a,glm.vec3(1,0,0))
    mvp = p * v * m
    glUniformMatrix4fv(mvpId,1,GL_FALSE,glm.value_ptr(mvp))
    desenhaCubo(idVa)

    #CUBO 2o quadrante
    m = glm.translate(glm.vec3(-3,3,0)) * glm.rotate(a,glm.vec3(0,1,0))
    mvp = p * v * m
    glUniformMatrix4fv(mvpId,1,GL_FALSE,glm.value_ptr(mvp))
    desenhaCubo(idVa)

    #CUBO 3o quadrante
    m = glm.translate(glm.vec3(-3,-3,0)) * glm.rotate(-a,glm.vec3(0,1,0))
    mvp = p * v * m
    glUniformMatrix4fv(mvpId,1,GL_FALSE,glm.value_ptr(mvp))
    desenhaCubo(idVa)

    #CUBO 4o quadrante
    m = glm.translate(glm.vec3(3,-3,0)) * glm.rotate(-a,glm.vec3(1,0,0))
    mvp = p * v * m
    glUniformMatrix4fv(mvpId,1,GL_FALSE,glm.value_ptr(mvp))
    desenhaCubo(idVa)
    a += 0.05

def createShaderProgram(shader):
    progId = None
    ids = []
    for shaderType, shaderSource in shader.items():
        shaderId = glCreateShader(shaderType)
        ids.append(shaderId)
        glShaderSource(shaderId,[shaderSource])
        glCompileShader(shaderId)
        status = glGetShaderiv(shaderId,GL_COMPILE_STATUS)
        if not status:
            print(glGetShaderInfoLog(shaderId))
            return None
    if len(ids) > 0:
        progId = glCreateProgram()
        for shaderId in ids:
            glAttachShader(progId,shaderId)
        glLinkProgram(progId)
        status = glGetProgramiv(progId,GL_LINK_STATUS)
        if not status:
            print(glGetProgramInfoLog(progId))
            for shaderId in ids:
                glDetachShader(progId,shaderId)
            glDeleteProgram(progId)
            progId = None
        for shaderId in ids:
            glDeleteShader(shaderId)
    return progId

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
window = sdl2.SDL_CreateWindow(b"Cubo", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_SHOWN)
if not window:
    sys.stderr.write("Error: Could not create window\n")
    exit(1)
sdl2.SDL_GL_CreateContext(window)
glEnable(GL_DEPTH_TEST)
glEnable(GL_MULTISAMPLE)
running = True
event = sdl2.SDL_Event()
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False
        if event.type == sdl2.events.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                running = False
    desenha()
    sdl2.SDL_GL_SwapWindow(window)
