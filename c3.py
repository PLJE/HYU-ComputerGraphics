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

where = 0
def render():
    global perspective ,zoom, u,v,w,up,o,azi,ele,zoomAng ,where , frame_num
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if perspective == 0 :
        glOrtho(-zooming,zooming,-zooming,zooming,-20,20)
    elif perspective == 1 :
        gluPerspective(zoomAng,1,1,20)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    getvec()
    
    gluLookAt(o[0]+10*w[0],o[1]+10*w[1],o[2]+10*w[2],o[0],o[1],o[2],0,up,0)
    
    drawGrid()

    glEnable(GL_LIGHTING)   
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_NORMALIZE)
    lightPos1 = (3.,4.,5.,1.) #point light
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos1)
    lightPos2 = (-3.,4.,-5.,1.) #point light
    glLightfv(GL_LIGHT1 , GL_POSITION , lightPos2)

    lightColor1 = (1.,1.,0.,1.) 
    lightColor2 = (1.,0.,1.,1.)
    ambientLightColor1 = (.1,.1,.0,1.)
    ambientLightColor2 = (.1,.0,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor1)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor2)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor2)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor2)
    objectColor = (1.,0.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    #glColor3ub(200,0,200)

    if animate == 1:
        where+=1
        if where >= frame_num:
            where = 0
    #glColor3ub(255,255,0)
    Animate()

    glDisable(GL_LIGHTING)

animate = 0
frame_num = 0 
channel = [] 
joints = [] #including root
offset = []
motion = []
def drop_callback(window, path):
    file = open(path[0])
    
    cnt = 0
    FPS=0
    joint_num=0

    global channel,joints ,offset , motion ,frame_num , animate

    animate = 0

    frame_num=0
    channel=[]
    joints=[]
    offset=[]
    motion=[]
    
    while True:
        line = file.readline()
        line = line.strip()
        if not line:
            break
        if line == 'HIERARCHY' :
            cnt = 1
            continue
        elif line == 'MOTION':
            cnt = 2
            continue
        
        if cnt == 1 : #hierarchy
            parsing = line.split()
            if parsing[0] == 'ROOT' :
                list.append(joints , parsing[1])
                joint_num+=1
            elif parsing[0] == 'JOINT':
                list.append(joints, parsing[1])
                joint_num+=1
            elif parsing[0] == '{':
                list.append(channel,'start')
            elif parsing[0] == '}':
                list.append(channel, 'end')
            elif parsing[0] == 'OFFSET':
                list.append(offset, float(parsing[1]))
                list.append(offset, float(parsing[2]))
                list.append(offset, float(parsing[3]))
            elif parsing[0] == 'CHANNELS':
                for par in parsing[2:]:
                    par = par.upper()
                    if par == 'XPOSITION' :
                        list.append(channel,'XP')
                    elif par == 'YPOSITION':
                        list.append(channel, 'YP')
                    elif par == 'ZPOSITION':
                        list.append(channel, 'ZP')
                    elif par == 'XROTATION':
                        list.append(channel, 'XR')
                    elif par == 'YROTATION':
                        list.append(channel, 'YR')
                    elif par == 'ZROTATION':
                        list.append(channel, 'ZR')
            elif parsing[0] == 'END Site':
                continue
        elif cnt == 2 : #motion
            parsing = line.split()
            if parsing[0]=='Frames:':
                frame_num = int(parsing[1])
            elif parsing[0] == 'Frame' :
                FPS = 1./float(parsing[2])
            else :
                oneframe =[]
                for i in parsing:
                    list.append(oneframe, float(i))
                list.append(motion, oneframe)

    print('1. File name : ' + path[0])
    print('2. Numbef of frames : ' + str(frame_num))
    print('3. FPS : ' + str(FPS))
    print('4. Number of joints(including root) : ' + str(joint_num))
    print('5. List of all joint names : ')
    for i in joints:
        print(i+" ")
    #print(motion[0])

def norm(v):
    return np.sqrt(np.dot(v, v))

def drawBox(i,f,j):
    glPushMatrix()
    glTranslatef(-i/2,-f/2,-j/2)
    b = np.array([-i,-f,-j])
    bsize = norm(b)
    b=b/bsize
    if np.dot(b,np.array([1,0,0]))!=0:
        glScalef(2*bsize,1,1)
    else :
        glScalef(1,2*bsize,1)
    #drawFrame()
    varr = np.array([
            ( -.1 ,  .1 ,  .1 ), # v0
            (  .1 ,  .1 ,  .1 ), # v1
            (  .1 , -.1 ,  .1 ), # v2
            ( -.1 , -.1 ,  .1 ), # v3
            ( -.1 ,  .1 , -.1 ), # v4
            (  .1 ,  .1 , -.1 ), # v5
            (  .1 , -.1 , -.1 ), # v6
            ( -.1 , -.1 , -.1 ), # v7
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
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3,GL_FLOAT,3*varr.itemsize ,varr)
    glDrawElements(GL_TRIANGLES,iarr.size,GL_UNSIGNED_INT,iarr)
    glPopMatrix()
lines = 1
def Animate():
    global channel,joints ,offset , motion ,where, animate,lines
    offidx = 0
    cnt = 0
    #for where in range(0,frame_num):
    for what in channel :
            if what == 'start':
                glPushMatrix()
                glTranslatef(offset[offidx]/10,offset[offidx+1]/10,offset[offidx+2]/10)
                #glColor3ub(255,255,0)
                if lines == 1:
                    glBegin(GL_LINES)
                    glVertex3f(0,0,0)
                    glVertex3f(-offset[offidx]/10,-offset[offidx+1]/10,-offset[offidx+2]/10)
                    glEnd()
                    #drawFrame()
                if lines ==0 :
                    drawBox(offset[offidx]/10,offset[offidx+1]/10,offset[offidx+2]/10)
                offidx+=3
            elif what == 'end':
                glPopMatrix()
            else :
                if animate ==1:
                    if what == 'XP':
                        glTranslatef(motion[where][cnt]/10,0,0)
                    elif what == 'YP':
                        glTranslatef(0,motion[where][cnt]/10,0)
                    elif what == 'ZP':
                        glTranslatef(0,0,motion[where][cnt]/10)
                    elif what =='XR':
                        glRotatef(motion[where][cnt],1,0,0)
                    elif what =='YR':
                        glRotatef(motion[where][cnt],0,1,0)
                    elif what =='ZR':
                        glRotatef(motion[where][cnt],0,0,1)
                    cnt+=1
                    
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([.1,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,.1,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,.1]))
    glEnd()        

def drawGrid():
    glBegin(GL_LINES)
    glColor3ub(150,150,150)
    for i in np.linspace(-5,5,50):
        glVertex3fv(np.array([-5,0,i]))
        glVertex3fv(np.array([5,0,i]))
        glVertex3fv(np.array([i,0,-5]))
        glVertex3fv(np.array([i,0,5]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global perspective, animate , lines
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_V:
            if perspective==0:
                perspective=1
            else:
                perspective=0
        if key==glfw.KEY_SPACE:
            animate = 1
            #print('press space')
        if key==glfw.KEY_A :
            if lines==0:
                lines =1
            elif lines==1:
                lines =0


def scroll_callback(window, xoffset, yoffset):
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
                        
    elif button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            pre = glfw.get_cursor_pos(window)
            cur=glfw.get_cursor_pos(window)
            right=1
        elif action ==glfw.RELEASE:
            right=0

def cursor_callback(window, xpos, ypos):
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
    window = glfw.create_window(1200,1200,'Animation', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_drop_callback(window,drop_callback)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
