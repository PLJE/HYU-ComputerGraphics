import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

perspective = 0
hierar = 0

togshading =0
wireframe = 1

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

varr = np.array([] , 'float32')
dvarr = np.array([] ,'float32')
narr = np.array([] ,'float32')
fnarr = np.array([] ,'float32')
svarr = np.array([] ,'float32')
diarr = np.array([])

#1 2 3 for hierarchical 
varr1 = np.array([] , 'float32')
dvarr1 = np.array([] ,'float32')
narr1 = np.array([] ,'float32')
fnarr1 = np.array([] ,'float32')
svarr1 = np.array([] ,'float32')
diarr1 = np.array([])

varr2 = np.array([] , 'float32')
dvarr2 = np.array([] ,'float32')
narr2 = np.array([] ,'float32')
fnarr2 = np.array([] ,'float32')
svarr2 = np.array([] ,'float32')
diarr2 = np.array([])

varr3 = np.array([] , 'float32')
dvarr3 = np.array([] ,'float32')
narr3 = np.array([] ,'float32')
fnarr3 = np.array([] ,'float32')
svarr3 = np.array([] ,'float32')
diarr3 = np.array([])

    
def render():
    global perspective ,zoom, u,v,w,up,o,azi,ele,zoomAng ,hierar
    global varr1,dvarr1,narr1,fnarr1,svarr1,diarr1
    global varr2,dvarr2,narr2,fnarr2,svarr2,diarr2
    global varr3,dvarr3,narr3,fnarr3,svarr3,diarr3
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if wireframe==1:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE)
    elif wireframe==0:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if perspective == 0 :
        glOrtho(-zooming,zooming,-zooming,zooming,-20,20)
    elif perspective == 1 :
        gluPerspective(zoomAng,1,1,20)

    
    getvec()

    
    gluLookAt(o[0]+10*w[0],o[1]+10*w[1],o[2]+10*w[2],o[0],o[1],o[2],0,up,0)
    
    glMatrixMode(GL_MODELVIEW)
    drawFrame()
    drawGrid()

    glEnable(GL_LIGHTING)   
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_NORMALIZE)
    lightPos1 = (3.,4.,5.,1.) #point light
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos1)
    lightPos2 = (-3.,4.,-5.,1.) #point light
    glLightfv(GL_LIGHT1 , GL_POSITION , lightPos2)

    lightColor1 = (1.,1.,0.,1.) #yellow
    lightColor2 = (1.,0.,1.,1.) #purple
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor1)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor2)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor2)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 15)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    #glDisable(GL_LIGHTING) #if you disable here , object color is different

    glLoadIdentity()
    t = glfw.get_time()
    if hierar == 1:
        glPushMatrix()
        glTranslatef(-0.2,0.,0.)
        glRotatef(t*(180/np.pi) ,0,1,0)
        glPushMatrix()
        glScalef(.3,.3,.3)
        if togshading ==0 :
            hdraw_glDrawArray(dvarr1)
        else:
            hdraw_glDrawElements(svarr1,diarr1)
        glPopMatrix()
        #drawFrame()
        
        glPushMatrix()
        glTranslatef(-0.5,1.2,0.)
        glRotatef(180 ,0.,0.,1.)
        glRotatef(30*np.sin(t),1.,0.,0.)
        glPushMatrix()
        glScalef(.3,.3,.3)
        if togshading==0:
            hdraw_glDrawArray(dvarr2)
        else:
            hdraw_glDrawElements(svarr2,diarr2)
        glPopMatrix()
        #drawFrame()

        glPushMatrix()
        glTranslatef(0.,0.,2.5)
        glRotatef(90,1.,0.,0.)
        glTranslatef(0,0,1)
        glTranslatef(0,0,np.sin(t))
        glPushMatrix()
        glScalef(.3,.3,.3)
        if togshading==0:
            hdraw_glDrawArray(dvarr3)
        else:
            hdraw_glDrawElements(svarr3,diarr3)
        glPopMatrix()
        #drawFrame()
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
        
    
    if togshading == 0 and hierar== 0 :
        draw_glDrawArray()
    elif togshading ==1 and hierar == 0 :
        draw_glDrawElements()
        
    glDisable(GL_LIGHTING)

def hdraw_glDrawElements(svarr,diarr): 
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*svarr.itemsize , svarr)
    glVertexPointer(3,GL_FLOAT,6*svarr.itemsize , ctypes.c_void_p(svarr.ctypes.data + 3*svarr.itemsize))
    glDrawElements(GL_TRIANGLES , diarr.size , GL_UNSIGNED_INT , diarr)
def hdraw_glDrawArray(dvarr): 
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT,6*dvarr.itemsize , dvarr)
    glVertexPointer(3,GL_FLOAT , 6*dvarr.itemsize , ctypes.c_void_p(dvarr.ctypes.data + 3*dvarr.itemsize))
    glDrawArrays(GL_TRIANGLES , 0, int(dvarr.size/6))
    
def parsing(f):
    var=[]
    dvar=[]
    diar=[]
    nar=[]
    fnar=[]
    svar=[]

    while True:
        line = f.readline()
        if not line:
            break
        parsing = line.split()
        if len(parsing)==0 :
            continue
        if parsing[0] =='v':
            list.append(var,(float(parsing[1]),float(parsing[2]),float(parsing[3])))
            list.append(fnar, np.array([0,0,0],'float32') )
        elif parsing[0]=='vn' :
            list.append(nar , (float(parsing[1]),float(parsing[2]),float(parsing[3])))
        elif parsing[0]== 'f':
            f1 = parsing[1].split('/')
            v1 = int(f1[0])
            vn1 = int(f1[2])
            v2 = 0
            vn2= 0
            v3=0
            vn3=0
            for parsing in parsing[2:]:
                p = parsing.split('/')
                v3 = int(p[0])
                vn3 = int(p[2])
                if v3!=0 and v2!=0 :
                    list.append(diar, (v1-1,v2-1 ,v3-1))

                    list.append(dvar , nar[vn1-1])
                    list.append(dvar , var[v1-1])
                    list.append(dvar , nar[vn2-1])
                    list.append(dvar , var[v2-1])
                    list.append(dvar , nar[vn3-1])
                    list.append(dvar , var[v3-1])

                    smoothnormal = np.cross(np.array(var[v2-1])-np.array(var[v1-1]),np.array(var[v3-1])-np.array(var[v1-1]))
                    smoothnormal /= np.sqrt(np.dot(smoothnormal , smoothnormal)) #for unit vector

                    fnar[v1-1]+= smoothnormal
                    fnar[v2-1]+= smoothnormal
                    fnar[v3-1]+= smoothnormal
                v2 = v3
                vn2 = vn3
    for i in range(len(var)):
        list.append(svar , fnar[i]/np.sqrt(np.dot(fnar[i],fnar[i])))
        list.append(svar , var[i])
    svar = np.array(svar, 'float32')
            
    dvar = np.array(dvar,'float32')
    diar = np.array(diar)
    var = np.array(var)
    nar = np.array(nar)

    return var,dvar,nar,fnar,svar,diar

def draw_glDrawElements(): #for smooth shading. use face normal here. similar to lab7-2
    global svarr ,diarr
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*svarr.itemsize , svarr)
    glVertexPointer(3,GL_FLOAT,6*svarr.itemsize , ctypes.c_void_p(svarr.ctypes.data + 3*svarr.itemsize))
    glDrawElements(GL_TRIANGLES , diarr.size , GL_UNSIGNED_INT , diarr)
def draw_glDrawArray(): #using normal data in obj files
    global dvarr
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT,6*dvarr.itemsize , dvarr)
    glVertexPointer(3,GL_FLOAT , 6*dvarr.itemsize , ctypes.c_void_p(dvarr.ctypes.data + 3*dvarr.itemsize))
    glDrawArrays(GL_TRIANGLES , 0, int(dvarr.size/6))
    
def drop_callback(window, path):
    file = open(path[0])
    global varr, narr,dvarr, diarr ,fnarr , svarr

    varr=[]
    dvarr=[]
    diarr=[]
    narr=[]
    fnarr=[]
    svarr=[]

    totalface = 0
    three=0
    four=0
    more=0
    while True:
        line = file.readline()
        if not line:
            break
        parsing = line.split()
        if len(parsing)==0 :
            continue
        #ignore other things , only v, vn, f
        if parsing[0] =='v':
            list.append(varr,(float(parsing[1]),float(parsing[2]),float(parsing[3])))
            list.append(fnarr, np.array([0,0,0],'float32') )
        elif parsing[0]=='vn' :
            list.append(narr , (float(parsing[1]),float(parsing[2]),float(parsing[3])))
        elif parsing[0]== 'f':
            totalface+=1
            if len(parsing) == 4 :
                three+=1
            elif len(parsing) == 5 :
                four+=1
            elif len(parsing)>5:
                more+=1
            f1 = parsing[1].split('/')
            v1 = int(f1[0])
            vn1 = int(f1[2])
            v2 = 0
            vn2= 0
            v3=0
            vn3=0
            #for extra credit
            #to render a n-polygon(n>3) as a set of triangles "triangulation"
            #divide to several triangles
            for parsing in parsing[2:]:
                p = parsing.split('/')
                v3 = int(p[0])
                vn3 = int(p[2])
                if v3!=0 and v2!=0 :
                    list.append(diarr, (v1-1,v2-1 ,v3-1))

                    list.append(dvarr , narr[vn1-1])
                    list.append(dvarr , varr[v1-1])
                    list.append(dvarr , narr[vn2-1])
                    list.append(dvarr , varr[v2-1])
                    list.append(dvarr , narr[vn3-1])
                    list.append(dvarr , varr[v3-1])

                    smoothnormal = np.cross(np.array(varr[v2-1])-np.array(varr[v1-1]),np.array(varr[v3-1])-np.array(varr[v1-1]))
                    smoothnormal /= np.sqrt(np.dot(smoothnormal , smoothnormal)) #for unit vector

                    fnarr[v1-1]+= smoothnormal
                    fnarr[v2-1]+= smoothnormal
                    fnarr[v3-1]+= smoothnormal
                v2 = v3
                vn2 = vn3
    for i in range(len(varr)):
        list.append(svarr , fnarr[i]/np.sqrt(np.dot(fnarr[i],fnarr[i])))
        list.append(svarr , varr[i])
    svarr = np.array(svarr, 'float32')
            
    dvarr = np.array(dvarr,'float32')
    diarr = np.array(diarr) #index array
    varr = np.array(varr)
    narr = np.array(narr)
    print('1. File name : ' + path[0])
    print('2. Total number of faces : ' + str(totalface))
    print('3. Number of faces with 3 vertices :' +str(three))
    print('4. Number of faces with 4 vertices :' +str(four))
    print('5. Number of faces with more than 4 vertices :' + str(more))
            
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
    glColor3ub(102,102,102)
    for i in np.linspace(-5,5,50):
        glVertex3fv(np.array([-5,0,i]))
        glVertex3fv(np.array([5,0,i]))
        glVertex3fv(np.array([i,0,-5]))
        glVertex3fv(np.array([i,0,5]))
    glEnd()
    
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
                        
    elif button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            pre = glfw.get_cursor_pos(window)
            cur=glfw.get_cursor_pos(window)
            right=1
        elif action ==glfw.RELEASE:
            right=0
def key_callback(window, key, scancode, action, mods):
    global togshading , perspective ,wireframe ,hierar
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_S:
            if togshading==0 :
                togshading =1
            elif togshading == 1:
                togshading =0
        if key==glfw.KEY_V:
            if perspective==0:
                perspective=1
            else:
                perspective=0
        if key==glfw.KEY_Z:
            if wireframe==1:
                wireframe=0
            else:
                wireframe=1
        if key==glfw.KEY_H:
            if hierar==1:
                hierar = 0
            else:
                hierar = 1
            
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
    window = glfw.create_window(800,800,'ObjViewer', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_drop_callback(window,drop_callback)

    global varr1,dvarr1,narr1,fnarr1,svarr1,diarr1
    global varr2,dvarr2,narr2,fnarr2,svarr2,diarr2
    global varr3,dvarr3,narr3,fnarr3,svarr3,diarr3

    f=open('bone.obj',mode='r',encoding='utf-8')
    varr1,dvarr1,narr1,fnarr1,svarr1,diarr1 = parsing(f)
    f=open('hand.obj',mode='r',encoding='utf-8')
    varr2,dvarr2,narr2,fnarr2,svarr2,diarr2 = parsing(f)
    f=open('coin.obj',mode='r',encoding='utf-8')
    varr3,dvarr3,narr3,fnarr3,svarr3,diarr3 = parsing(f)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
