import glfw
from OpenGL.GL import *
import numpy as np

chk=3

def render(n):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    glColor3f(0.0,1.1,0.0)
    v = np.linspace(0.0,360.0,13)
    for i in range(12):
        glVertex2f(np.cos(v[i]*(np.pi/180)) , np.sin(v[i]*(np.pi/180)) )
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(0,0)
    glVertex2f(np.cos(v[n]*(np.pi/180)) , np.sin(v[n]*(np.pi/180)) )
    glEnd()

def key_callback(window,key,scancode, action, mods):
    v = np.linspace(0.0,360.0,13)
    global chk
    if key==glfw.KEY_1:
        if action==glfw.PRESS:
            chk=2
    elif key==glfw.KEY_2:
        if action==glfw.PRESS:
            chk=1
    elif key==glfw.KEY_3:
        if action==glfw.PRESS:
            chk=0
    elif key==glfw.KEY_4:
        if action==glfw.PRESS:
            chk=11
    elif key==glfw.KEY_5:
        if action==glfw.PRESS:
            chk=10
    elif key==glfw.KEY_6:
        if action==glfw.PRESS:
            chk=9
    elif key==glfw.KEY_7:
        if action==glfw.PRESS:
            chk=8
    elif key==glfw.KEY_8:
        if action==glfw.PRESS:
            chk=7
    elif key==glfw.KEY_9:
        if action==glfw.PRESS:
            chk=6
    elif key==glfw.KEY_0:
        if action==glfw.PRESS:
            chk=5
    elif key==glfw.KEY_Q:
        if action==glfw.PRESS:
            chk=4
    elif key==glfw.KEY_W:
        if action==glfw.PRESS:
            chk=3
            
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2019097347" ,None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render(chk)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
    
