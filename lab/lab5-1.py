import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


def drawFrame():
 glBegin(GL_LINES)
 glColor3ub(255, 0, 0)
 glVertex2fv(np.array([0.,0.]))
 glVertex2fv(np.array([1.,0.]))
 glColor3ub(0, 255, 0)
 glVertex2fv(np.array([0.,0.]))
 glVertex2fv(np.array([0.,1.]))
 glEnd()
 
def drawTriangle():
 glBegin(GL_TRIANGLES)
 glVertex2fv(np.array([0.,.5]))
 glVertex2fv(np.array([0.,0.]))
 glVertex2fv(np.array([.5,0.]))
 glEnd()
 
def render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()
    #first
    drawFrame()
    glColor3ub(255, 255, 255)
    drawTriangle()


    #second
    glRotate(30,0,0,1)
    glMultMatrixf(np.array([[1,0,0,0.6],
                           [0,1,0,0],
                           [0,0,1,0],
                           [0,0,0,1]]).T)
    drawFrame()
    glColor3ub(255, 0, 0)
    drawTriangle()

    #third
    glLoadIdentity()
    
    glMultMatrixf(np.array([[1,0,0,0.6],
                           [0,1,0,0],
                           [0,0,1,0],
                           [0,0,0,1]]).T)
    glRotate(30,0,0,1)
    drawFrame()
    glColor3ub(0, 0, 255)#blue
    #print('draw blue')
    drawTriangle()



    


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2019097347', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
