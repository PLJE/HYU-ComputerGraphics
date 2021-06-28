import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *

def drawTriangle():
 glBegin(GL_TRIANGLES)
 glVertex2fv(np.array([0.,.5]))
 glVertex2fv(np.array([0.,0.]))
 glVertex2fv(np.array([.5,0.]))
 glEnd()

var=[4]


def render():
 glClear(GL_COLOR_BUFFER_BIT)
 glLoadIdentity()
 
 glBegin(GL_LINES)
 glColor3ub(255, 0, 0)
 glVertex2fv(np.array([0.,0.]))
 glVertex2fv(np.array([1.,0.]))
 glColor3ub(0, 255, 0)
 glVertex2fv(np.array([0.,0.]))
 glVertex2fv(np.array([0.,1.]))
 glEnd()
 
 glColor3ub(255, 255, 255)
 
 global var
 for i in reversed(var):
     if(i==0):
         glTranslatef(-0.1,0.,0.)
     elif(i==1):
         glTranslatef(0.1,0.,0.)
     elif(i==2):
         glRotate(10,0,0,1)
     elif(i==3):
         glRotate(-10,0,0,1)
     elif(i==4):
         I = np.identity(4)
         glMultMatrixf(I.T) 
 drawTriangle()

def key_callback(window, key, scancode, action , mods):
    global var
    if key==glfw.KEY_Q:
        if action==glfw.PRESS or action==glfw.REPEAT:
            var.append(0)
    elif key==glfw.KEY_E:
        if action==glfw.PRESS or action==glfw.REPEAT:
            var.append(1)
    elif key==glfw.KEY_A:
        if action==glfw.PRESS or action==glfw.REPEAT:
            var.append(2)
    elif key==glfw.KEY_D:
        if action==glfw.PRESS or action==glfw.REPEAT:
            var.append(3)
    elif key==glfw.KEY_1:
        if action==glfw.PRESS or action==glfw.REPEAT:
            var.clear()
            var.append(4)
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2019097347", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window,key_callback)
    glfw.make_context_current(window)

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
