import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.

infer =1

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -1 ,  1 ,  1 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  1 ,  1 ,  1 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  1 , -1 ,  1 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -1 , -1 ,  1 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -1 ,  1 , -1 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  1 ,  1 , -1 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  1 , -1 , -1 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,3.]))
    glEnd()
def exp(v):
    angle = l2norm(v)
    axis = normalized(v)
    sin = np.sin(angle)
    cos = np.cos(angle)
    x = axis[0]
    y = axis[1]
    z = axis[2]

    return np.array([[cos + x*x*(1-cos) , x*y*(1-cos)-z*sin , x*z*(1-cos)+y*sin],
                     [x*y*(1-cos)+z*sin , cos+y*y*(1-cos) , y*z*(1-cos)-x*sin],
                     [x*z*(1-cos)-y*sin, y*z*(1-cos)+x*sin , cos+z*z*(1-cos)]])
def log(R):
    angle = np.arccos((R[0,0]+R[1,1]+R[2,2]-1)/2)
    x = (R[2,1]-R[1,2])/2*np.sin(angle)
    y = (R[0,2]-R[2,0])/2*np.sin(angle)
    z = (R[1,0]-R[0,1])/2*np.sin(angle)

    v = np.array([x,y,z])
    v = normalized(v)

    return v * angle

def l2norm(v):
    return np.sqrt(np.dot(v, v))

def normalized(v):
    l = l2norm(v)
    return 1/l * np.array(v)
def slerp(R1,R2,t):
    return R1 @ exp( log(R1.T@R2)*t )

def XYZEulerToRotMat(euler):
    xang, yang, zang = euler
    Rx = np.array([[1,0,0,0],
                   [0, np.cos(xang), -np.sin(xang),0],
                   [0, np.sin(xang), np.cos(xang),0],
                   [0,0,0,1]])
    Ry = np.array([[np.cos(yang), 0, np.sin(yang),0],
                   [0,1,0,0],
                   [-np.sin(yang), 0, np.cos(yang),0],
                   [0,0,0,1]])
    Rz = np.array([[np.cos(zang), -np.sin(zang), 0,0],
                   [np.sin(zang), np.cos(zang), 0,0],
                   [0,0,1,0],
                   [0,0,0,1]])
    return Rx @ Ry @ Rz


def lerp(v1, v2, t):
    return (1-t)*v1 + t*v2

def render(ang):
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    objectColor = (1.,0.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    ####################red
    euler1 = np.array([np.radians(20),np.radians(30),np.radians(30)])
    red1 = np.identity(4)
    red1 = XYZEulerToRotMat(euler1)
    J1 = red1
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    red2 = np.identity(4)
    T1 = np.identity(4)
    T1[0][3] = 1.

    euler2 = np.array([np.radians(15),np.radians(30),np.radians(25)])
    red2 = XYZEulerToRotMat(euler2)
    J2 = red1 @ T1 @ red2
    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()
    
    ####################yellow

    euler1 = np.array([np.radians(45),np.radians(60),np.radians(40)])
    yel1 = np.identity(4)
    yel1 = XYZEulerToRotMat(euler1)
    J1 = yel1
    
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    objectColor = (1.,1.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    yel2 = np.identity(4)
    euler2 = np.array([np.radians(25),np.radians(40),np.radians(40)])
    yel2 = XYZEulerToRotMat(euler2)
    J2 = yel1 @ T1 @ yel2
    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()
    ###################### green
    euler1 = np.array([np.radians(60),np.radians(70),np.radians(50)])
    green1 = np.identity(4)
    green1 = XYZEulerToRotMat(euler1)
    J1 = green1
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    objectColor = (0.,1.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    euler2 = np.array([np.radians(40),np.radians(60),np.radians(50)])
    green2 = np.identity(4)
    green2 = XYZEulerToRotMat(euler2)
    J2 = green1 @ T1 @ green2
    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()
    ############################# blue
    euler1 = np.array([np.radians(80),np.radians(85),np.radians(70)])
    blue1 = np.identity(4)
    blue1 = XYZEulerToRotMat(euler1)
    J1 = blue1
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    objectColor = (0.,0.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    euler2 = np.array([np.radians(55),np.radians(80),np.radians(65)])
    blue2 = np.identity(4)
    blue2 = XYZEulerToRotMat(euler2)
    J2 = blue1 @ T1 @ blue2
    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()
    ########################

    t = (ang%90)/90

    R1 = np.identity(4)
    R2 = np.identity(4)
    R1[:3,:3] = slerp(red1[:3,:3] , yel1[:3,:3] ,t)
    R2[:3,:3] = slerp(red2[:3,:3] , yel2[:3,:3],t)

    R3 = np.identity(4)
    R4 = np.identity(4)
    R3[:3,:3] = slerp(yel1[:3,:3] , green1[:3,:3] ,t)
    R4[:3,:3] = slerp(yel2[:3,:3] , green2[:3,:3],t)

    R5 = np.identity(4)
    R6 = np.identity(4)
    R5[:3,:3] = slerp(green1[:3,:3] , blue1[:3,:3] ,t)
    R6[:3,:3] = slerp(green2[:3,:3] , blue2[:3,:3],t)

    global infer

    if t>0.98888888 :
        infer+=1

    if infer%3 ==1:
        M1=R1
        M2=R2
    if infer%3 ==2:
        M1=R3
        M2=R4
    if infer%3==0 :
        M1 = R5
        M2=R6
    
    glPushMatrix()
    glMultMatrixf((M1).T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glMultMatrixf((M1@T1@M2).T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    
    glDisable(GL_LIGHTING)
    
def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2019097347', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    count =0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        ang = count %360
        t = glfw.get_time()
        render(ang)
        count+=1
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
