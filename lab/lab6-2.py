import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()

def render():
     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
     glEnable(GL_DEPTH_TEST)
     glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
     glLoadIdentity()
     
     myFrustum(-1,1, -1,1, 1,10)
     myLookAt(np.array([5,3,5]), np.array([1,1,-1]), np.array([0,1,0]))
     
     # Above two lines must behave exactly same as the below two lines
     #glFrustum(-1,1, -1,1, 1,10)
     #gluLookAt(5,3,5, 1,1,-1, 0,1,0)
     
     drawFrame()
     
     glColor3ub(255, 255, 255)
     drawCubeArray()

def myFrustum(left, right, bottom, top,near,far):
    l = left
    r = right
    b = bottom
    t = top
    n = near
    f = far
    Mpers = np.array([[(2*n)/(r-l),0,(r+l)/(r-l),0],
                      [0,(2*n)/(t-b),(t+b)/(t-b),0],
                      [0,0,-(f+n)/(f-n),-2*f*n/(f-n)],
                      [0,0,-1,0]])
    glMultMatrixf(Mpers.T)
    
def myLookAt(eye, at, up):
    ea = eye-at
    w = ea / np.sqrt(np.dot(ea,ea) )
    
    cro = np.cross(up,w)
    u = cro / np.sqrt(np.dot(cro,cro))
    
    v = np.cross(w,u)
    
    MV = np.array([[u[0],v[0],w[0],eye[0]],
                  [u[1],v[1],w[1],eye[1]],
                  [u[2],v[2],w[2],eye[2]],
                  [0,0,0,1]])
    
    #multiple inverse matrix
    glMultMatrixf(np.linalg.inv(MV).T)

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
