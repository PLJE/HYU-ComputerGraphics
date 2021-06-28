import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

perspective = 0

zoomAng = 40
zooming = 2
o = np.array([0.,0.,0.])
u = np.array([1.,0.,0.])
v = np.array([0.,1.,0.])
w = np.array([0.,0.,1.])
up = 1.

azi = 0
ele = 0

def getvec():
    global ele, azi, w, u,v

    w = np.array([np.sin(azi)*np.cos(ele) , np.sin(ele) , np.cos(ele)*np.cos(azi)])
    u=np.cross(np.array([0,up,0]),w)
    u = u/np.sqrt(np.dot(u,u))

    v=np.cross(w,u)
    v=v/np.sqrt(np.dot(v,v))
    
def render():
    global perspective ,zoom, u,v,w,up,o,azi,ele,zoomAng
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    glLoadIdentity()

    if perspective == 0 :
        glOrtho(-zooming,zooming,-zooming,zooming,-20,20)
    elif perspective == 1 :
        gluPerspective(zoomAng,1,1,20)

    
    getvec()
    
    gluLookAt(o[0]+10*w[0],o[1]+10*w[1],o[2]+10*w[2],o[0],o[1],o[2],0,up,0)
    
    drawFrame()
    drawGrid()
    
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def drawGrid():
    glBegin(GL_LINES)
    glColor3ub(255,255,255)
    for i in np.linspace(-5,5,50):
        glVertex3fv(np.array([-5,0,i]))
        glVertex3fv(np.array([5,0,i]))
        glVertex3fv(np.array([i,0,-5]))
        glVertex3fv(np.array([i,0,5]))
    glEnd()
        
def key_callback(window, key, scancode, action, mods):
    global perspective
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_V:
            if perspective==0:
                perspective=1
            else:
                perspective=0


def scroll_callback(window, xoffset, yoffset):
    #print('mouse wheel scroll: %d, %d'%(xoffset, yoffset))
    global zooming, zoomAng

    if yoffset < 0:
        zooming +=0.2
        if zoomAng < 175:
            zoomAng+=2

    else :
        if zooming > 0.2:
            zooming -=0.2
        if zoomAng > 2:
            zoomAng-=2
        

left = 0
right =0
pre = np.array([0,0])
cur = np.array([0,0])

def button_callback(window, button , action, mod):
    global azi, ele, left, right, up, pre, cu
    
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            pre = glfw.get_cursor_pos(window)
            cur = glfw.get_cursor_pos(window)
            left = 1
        elif action==glfw.RELEASE:
            left = 0
            circle = 2*np.pi
            
            if ele >=circle :
                while ele >= circle:
                    ele -= circle
            if ele <=0:
                while ele <= 0:
                    ele += circle
                    
            if azi >=circle :
                while azi >= circle :
                    azi -= circle
            if azi <=0:
                while azi <=0 : 
                    azi += circle
                
    elif button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            pre = glfw.get_cursor_pos(window)
            cur=glfw.get_cursor_pos(window)
            right=1
        elif action ==glfw.RELEASE:
            right=0

def cursor_callback(window, xpos, ypos):
    #print('mouse cursor moving: (%d, %d)'%(xpos, ypos))
    global azi, ele , left, right ,pre, cur, u,v,w,o,up

    if left == 1 :
        pre = cur
        cur = glfw.get_cursor_pos(window)
        ele -= (pre[1] - cur[1])/50
        
        if np.cos(ele) <= 0 :
            up = -1
        else :
            up = 1
        azi = azi + up * ( pre[0]-cur[0] )/50
        
    if right ==1 :
        pre = cur
        cur = glfw.get_cursor_pos(window)
        o += ( ((pre[0]-cur[0])*u) + ((pre[1]-cur[1])*v) )/150
        
def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'MyOpenGLViewer', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
