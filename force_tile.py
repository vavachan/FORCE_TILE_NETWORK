import numpy as np
import sys 
#import matplotlib.pyplot as plt
#import matplotlib.patches as patches
#from matplotlib import collections  as mc


class edge:
    #atoms=np.zeros(2)
    #vertices = []
    #self.vertices=[]
    def __init__(self, atom1, atom2):
        self.atoms=np.zeros(2)
        self.atoms[0]=atom1
        self.atoms[1]=atom2
        self.vertices=[]
    def add_vertex(self, v):
        self.vertices.append(v)

class vertex():
    def __init__(self):
        self.edges=[]
        self.cordinates=[]
    def add_edges(self,e):
        self.edges.append(e)
    def add_cordinate(self, x , y):
        self.cordinates.append([x,y])
    
N=int(sys.argv[2])
done=np.zeros(N)
number_of_forces=np.zeros(N)
Forces=np.loadtxt(sys.argv[1])
Force_tiles    = [ [] for i in range(N) ]
Forces_rand    = [ [] for i in range(N) ]
Forces_angles  = [ [] for i in range(N) ]
Force_clockwise= [ [] for i in range(N) ]
Neibhors=[ [] for i in range(N) ]
atoms=[]
atoms.append(0)
#atoms.append(162)
#atoms.append(1176)
#atoms.append(254)
#atoms.append(249)
#atoms.append(1251)
#atoms.append(1250)





#atoms.append(162)
# In this loop we arrange the forces as if they are acting on the particle which is at the center.
# As in one end of the force vector is kept at center. 
for f in range (0,len(Forces)):
    Forces_rand[int(Forces[f][0])].append([[Forces[f][3],Forces[f][4]],[0.,0.]])
    Forces_rand[int(Forces[f][1])].append([[-1.*Forces[f][3],-1.*Forces[f][4]],[0.,0.]])
    Neibhors[int(Forces[f][0])].append(int(Forces[f][1]))
    Neibhors[int(Forces[f][1])].append(int(Forces[f][0]))


edges_to_draw=[]
edges_all = []
vertices_all = []
#for F in Forces_rand[i]:
#    edges_to_draw.append([(F[0][0],F[0][1]),(F[1][0],F[1][1])])
    #print((F[0][0],F[0][1],F[1][0],F[1][1]))
    #plt.quiver(F[1][0],F[1][1],F[0][0],F[0][1])
#lt.plot()
#plt.show()
#exit()
for i in range (0,N):
#Looping through each particle
    if(len(Forces_rand[i])):
        # calculating the mod |F| of the first force.
        mod_first=(Forces_rand[i][0][0][0]*Forces_rand[i][0][0][0]+Forces_rand[i][0][0][1]*Forces_rand[i][0][0][1])**(0.5)
        nn=0
        # loop through the forces
        # Idea is to arrange these forces which are randomly arranged in the array 
        # in the clockwise manner.
        for f in Forces_rand[i]:
            # mod of these forces.
            mod=(f[0][0]*f[0][0]+f[0][1]*f[0][1])**(0.5)
            overlap=Forces_rand[i][0][0][0]*f[0][0]+Forces_rand[i][0][0][1]*f[0][1]
            angle=np.arccos(overlap/(mod*mod_first))
            #print(overlap/(mod*mod_first))
            cross_product=Forces_rand[i][0][0][0]*f[0][1]-Forces_rand[i][0][0][1]*f[0][0]
            if(cross_product>0):
                angle=2*np.pi-angle
            #print(overlap/(mod*mod_first),angle/(np.pi)*180,cross_product)
            Forces_angles[i].append([(angle/np.pi)*180,f,Neibhors[i][nn]])
            nn=nn+1
            
            #sumx=sumx+f[0][0]
            #sumy=sumy+f[0][1]
        number_of_forces[i]=nn
        Forces_angles[i].sort(key = lambda elem : elem[0])
        #print(Forces_angles[i])
#pri    nt(np.sort(np.array(Forces_angles[i]),axis=0))
        Force_clockwise[i]=(np.array(Forces_angles[i])[:,1:3])
####    ()
        #print(Force_clockwise[i])
####nt(Force_tiles[i])
####nt(sumx*sumx+sumy*sumy)
#for f in Force_clockwise[63]:
#    print(f[1])
orginx=0.;
orginy=0.;
first_atom=atoms[0]
f=Force_clockwise[first_atom][0]
j=f[1]
edges_all.append(edge(first_atom,j))
e=edges_all[len(edges_all)-1]
#edges_all[len(edges_all)-1]=first_atom
#edges_all[len(edges_all)-1].atoms[1]=j
atoms.append(j)
#print(first_atom,j)
#edges_all.append(e)
v1= vertex()
v2= vertex()
v1.add_edges(e)
v2.add_edges(e)
e.add_vertex(v1)
e.add_vertex(v2)
vertices_all.append(v1)
vertices_all.append(v2)
v1.add_cordinate(orginx,orginy)
v2.add_cordinate(orginx+f[0][0][0],orginy+f[0][0][1])
Force_tiles[first_atom].append([[orginx,orginy],[orginx+f[0][0][0],orginy+f[0][0][1]],j,e])
Force_tiles[j].append([[orginx+f[0][0][0],orginy+f[0][0][1]],[orginx,orginy],first_atom,e])
count=0
# THIS IS THE LIST OF ATOMS FOR WHICH WE NEED TO EVALUATE THE FT 
for i in atoms:
    count=count+1
    #len(Force_tiles[i])!=number_of_forces[i]):
    sumx=0.
    sumy=0.
    #Force_clockwise[i][:,1].index(Force_tiles[i][len(Force_tiles[i])-1][2])
    #print(i,len(Force_tiles[i]),int(number_of_forces[i]))
    # THIS IS THE LIST OF FORCES CORRESPONDING TO ATOM "i"
    forces_list=Force_clockwise[i][:,1]
    
    #print(forces_list)
    forces_left=forces_list
    # IN FORCES LEFT I WANT TO STORE ALL THE FORCES THAT ARE YET TO BE ADDED 
    # INTO THE FTN
    if(len(Force_tiles[i])-int(number_of_forces[i])):
        for f in Force_tiles[i]:
            #print(np.where(Force_clockwise[i][:,1] == f[2])[0][0])
            forces_left=np.delete(forces_left,np.where(forces_left == f[2])[0][0])
            #print(forces_left)
    else:
        forces_left=[]
#    print('**begin******')
    # LET US ADD THESE FORCES TO THE FTN
    while(len(forces_left)>0):
        for f in forces_left:
            # FOR EACH FORCE WHICH BELONGS TO PARTICLE "i" , WE FIND THE INDEX OF THAT FORCE IN 
            # Force_clockwise  ARRAY.
            f_index=(np.where(Force_clockwise[i][:,1] == f)[0][0])
            # NOW WE FIND THE INDEX OF THE NEXT FORCE IN THE CLOCKWISE ORDER 
            # AND THE PREVIOUS FORCE IN THE CLOCKWISE ORDER.

            prev_in_order=int(Force_clockwise[i][int((f_index-1)%number_of_forces[i])][1])
            next_in_order=int(Force_clockwise[i][int((f_index+1)%number_of_forces[i])][1])
            #print(f_index,prev_in_order,forces_left)
            #print(f_index,next_in_order,forces_left)
            #print(np.array(Force_tiles[i])[:,2])
            #if(len(np.where(forces_left == prev_in_order)[0])>0):
            #    print(np.where(forces_left == prev_in_order)[0][0])
            # WE CHECK IF THE NEXT AND PREVIOUS FORCE IN THE CLOCKWISE ORDER EXISTS 
            # IN THE ATOM "i" FTN. 
            if_prev_exist=len(np.where(np.array(Force_tiles[i])[:,2] == prev_in_order)[0])
            if_next_exist=len(np.where(np.array(Force_tiles[i])[:,2] == next_in_order)[0])
            #next_ID=np.where(np.array(Force_tiles[i])[:,2] == next_in_order)[0][0][0]
            if( if_prev_exist >0):
                #prev_ID=np.where(np.array(Force_tiles[i])[:,2] == prev_in_order)[0][0][0]
                f_to_insert=Force_clockwise[i][f_index]
                j=f_to_insert[1]
                edges_all.append(edge(i,j))
                e=edges_all[len(edges_all)-1]
                #e = edge()
                #edges_all[len(edges_all)-1].atoms[0]=i
                #edges_all[len(edges_all)-1].atoms[1]=j
                prev_force=np.where(np.array(Force_tiles[i])[:,2] == prev_in_order)[0][0]
                prev_edge=Force_tiles[i][prev_force]
                if(prev_edge[3].atoms[0]==i ):
                    prev_edge[3].vertices[1].add_edges(e)
                    e.add_vertex(prev_edge[3].vertices[1])
                elif(prev_edge[3].atoms[1]==i):
                    prev_edge[3].vertices[0].add_edges(e)
                    e.add_vertex(prev_edge[3].vertices[0])
                #v.edges.append(prev_edge[3])
            #    print(i,j)
                if( if_next_exist ):
                    next_force=np.where(np.array(Force_tiles[i])[:,2] == next_in_order)[0][0]
                    next_edge=Force_tiles[i][next_force]
                    if(prev_edge[3].atoms[0]==i ):
                        if(next_edge[3].atoms[0]==i):
                            #prev_edge[3].vertices[1].add_edges(e)
                            #e.add_vertex(prev_edge[3].vertices[1])

                            e.add_vertex(next_edge[3].vertices[0])
                            next_edge[3].vertices[0].add_edges(e)

                            next_edge[3].vertices[0].add_cordinate(prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                    #        print("1,1a",next_edge[3].vertices[0].cordinates[len(next_edge[3].vertices[0].cordinates)-2],prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                            prev_edge[3].vertices[1].add_cordinate(next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                    #        print("1.2a",prev_edge[3].vertices[1].cordinates[len(prev_edge[3].vertices[1].cordinates)-2],next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                        elif(next_edge[3].atoms[1]==i):
                            #prev_edge[3].vertices[1].add_edges(e)
                            #e.add_vertex(prev_edge[3].vertices[1])

                            e.add_vertex(next_edge[3].vertices[1])
                            next_edge[3].vertices[1].add_edges(e)

                            next_edge[3].vertices[1].add_cordinate(prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                    #        print("1,1b",next_edge[3].vertices[1].cordinates[len(next_edge[3].vertices[1].cordinates)-2],prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                            prev_edge[3].vertices[1].add_cordinate(next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                    #        print("1.2b",prev_edge[3].vertices[1].cordinates[len(prev_edge[3].vertices[1].cordinates)-2],next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                    elif(prev_edge[3].atoms[1]==i):
                        if( next_edge[3].atoms[0]==i):
                            #prev_edge[3].vertices[0].add_edges(e)
                            #e.add_vertex(prev_edge[3].vertices[0])

                            e.add_vertex(next_edge[3].vertices[0])
                            next_edge[3].vertices[0].add_edges(e)

                            next_edge[3].vertices[0].add_cordinate(prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                    #        print("1,1c",next_edge[3].vertices[0].cordinates[len(next_edge[3].vertices[0].cordinates)-2],prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                            prev_edge[3].vertices[0].add_cordinate(next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                    #        print("1.2c",prev_edge[3].vertices[0].cordinates[len(prev_edge[3].vertices[0].cordinates)-2],next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                        elif(next_edge[3].atoms[1]==i):
                            #prev_edge[3].vertices[0].add_edges(e)
                            #e.add_vertex(prev_edge[3].vertices[0])

                            e.add_vertex(next_edge[3].vertices[1])
                            next_edge[3].vertices[1].add_edges(e)

                            next_edge[3].vertices[1].add_cordinate(prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                    #        print("1,1c",next_edge[3].vertices[1].cordinates[len(next_edge[3].vertices[1].cordinates)-2],prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                            prev_edge[3].vertices[0].add_cordinate(next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                    #        print("1.2c",prev_edge[3].vertices[0].cordinates[len(prev_edge[3].vertices[0].cordinates)-2],next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                        
                else : 
                    neighb=j
                    prev_neigh=i
                    while(1):
                        #print(neighb,prev_neigh)
                        f_j_index=(np.where(Force_clockwise[neighb][:,1] == prev_neigh)[0][0])
                        prev_j_in_order=int(Force_clockwise[neighb][int((f_j_index-1)%number_of_forces[neighb])][1])
                    #next_j_in_order=int(Force_clockwise[j][int((f_index+1)%number_of_forces[j])][1])
                        #print(f,Force_clockwise[neighb][:,1],j,prev_j_in_order,Force_tiles[neighb])
                    
                        if(len(Force_tiles[neighb])):
                            if_j_prev_exist=len(np.where(np.array(Force_tiles[neighb])[:,2] == prev_j_in_order)[0])
                            #print(if_j_prev_exist)
                            if(if_j_prev_exist):
                                prev_j_force=np.where(np.array(Force_tiles[neighb])[:,2] == prev_j_in_order)[0][0]
                                prev_j_edge=Force_tiles[neighb][prev_j_force]
                                if(prev_j_edge[3].atoms[0]==neighb ):
                                    prev_j_edge[3].vertices[1].add_edges(e)
                                    e.add_vertex(prev_j_edge[3].vertices[1])
                                elif(prev_j_edge[3].atoms[1]==neighb):
                                    prev_j_edge[3].vertices[0].add_edges(e)
                                    e.add_vertex(prev_j_edge[3].vertices[0])
                                break
                            else:
                                prev_neigh=neighb
                                neighb=prev_j_in_order                               
                                if(neighb==i):
                                    vertices_all.append(vertex())
                                    v = vertices_all[len(vertices_all)-1]
                                    v.add_edges(e)
                                    e.add_vertex(v)
                                    v.add_cordinate(prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                                    break
                        else:
                            prev_neigh=neighb
                            neighb=prev_j_in_order                            
                            if(neighb==i):
                                vertices_all.append(vertex())
                                v = vertices_all[len(vertices_all)-1]
                                v.add_edges(e)
                                e.add_vertex(v)
                                v.add_cordinate(prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                                break
                    #print("2",v.cordinates[len(v.cordinates)-2],prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1])
                    
                # NEW edge 
                # new vertex

                #print("prev",prev_force)
                Force_tiles[i].append([prev_edge[1],[prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1]],j,e])
                Force_tiles[j].append([[prev_edge[1][0]+f_to_insert[0][0][0],prev_edge[1][1]+f_to_insert[0][0][1]],prev_edge[1],i,e])
                forces_left=np.delete(forces_left,np.where(forces_left == f))
            elif(if_next_exist>0):
                next_force=np.where(np.array(Force_tiles[i])[:,2] == next_in_order)[0][0]
                f_to_insert=Force_clockwise[i][f_index]
                next_edge=Force_tiles[i][next_force]
                j=f_to_insert[1]
                edges_all.append(edge(i,j))
                e=edges_all[len(edges_all)-1]
                neighb=j
                prev_neigh=i
                while(1):
                    #print(neighb,prev_neigh)
                    f_j_index=(np.where(Force_clockwise[neighb][:,1] == prev_neigh)[0][0])
                    
                    next_j_in_order=int(Force_clockwise[neighb][int((f_j_index+1)%number_of_forces[neighb])][1])
                    #print(f,Force_clockwise[neighb][:,1],j,next_j_in_order,Force_tiles[neighb])
                    if(len(Force_tiles[neighb])):
                    #next_j_in_order=int(Force_clockwise[j][int((f_index+1)%number_of_forces[j])][1])
                        if_j_next_exist=len(np.where(np.array(Force_tiles[neighb])[:,2] == next_j_in_order)[0])
                        if(if_j_next_exist):
                            next_j_force=np.where(np.array(Force_tiles[neighb])[:,2] == next_j_in_order)[0][0]                
                            next_j_edge=Force_tiles[neighb][next_j_force]                    
                            if(next_j_edge[3].atoms[0]==neighb ):                    
                                next_j_edge[3].vertices[0].add_edges(e)                    
                                e.add_vertex(next_j_edge[3].vertices[0])                    
                            elif(next_j_edge[3].atoms[1]==neighb ):                    
                                next_j_edge[3].vertices[1].add_edges(e)                    
                                e.add_vertex(next_j_edge[3].vertices[1])
                            break
                        else:
                            prev_neigh=neighb
                            neighb=next_j_in_order                            
                            if(neighb==i):
                                vertices_all.append(vertex())                        
                                v = vertices_all[len(vertices_all)-1]                
                                v.add_edges(e)                                                
                                e.add_vertex(v)                                                
                                v.add_cordinate(next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                                break
                    else:
                        prev_neigh=neighb
                        neighb=next_j_in_order                        
                        if(neighb==i):
                            vertices_all.append(vertex())                        
                            v = vertices_all[len(vertices_all)-1]                
                            v.add_edges(e)                                                
                            e.add_vertex(v)                                                
                            v.add_cordinate(next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                            break
                #edges_all[len(edges_all)-1].atoms[0]=i
                #edges_all[len(edges_all)-1].atoms[1]=j
                #print(i,j)
                #print("3",v.cordinates[len(v.cordinates)-2],next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1])
                #print("next",next_force)
                #v.edges.append(next_edge[3])
                if(next_edge[3].atoms[0]==i):
                    e.add_vertex(next_edge[3].vertices[0])
                    next_edge[3].vertices[0].add_edges(e)
                elif(next_edge[3].atoms[1]==i):
                    e.add_vertex(next_edge[3].vertices[1])
                    next_edge[3].vertices[1].add_edges(e)
                #edges_all.append(edges_all[len(edges_all)-1])
                #vertices_all.append(v)

                Force_tiles[i].append([[next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1]],next_edge[0],j,e])
                Force_tiles[j].append([next_edge[0],[next_edge[0][0]-f_to_insert[0][0][0],next_edge[0][1]-f_to_insert[0][0][1]],i,e])
                forces_left=np.delete(forces_left,np.where(forces_left == f))
            #else:
                #print("curio")
            atoms.append(j)
    #if(count>100):
        #print(count)
    #    break
print(len(vertices_all),len(edges_all),len(vertices_all)-len(edges_all)+N)
alpha=100
vertices_dat=open("vertices.dat","w+")
vertices_dat_ar=open("vertices_ar.dat","w+")
invariants_dat = open ("invariants.dat","a+")
max_r=-9999
min_r=9999
for v in vertices_all:
  #  print(np.where( np.array(vertices_all) == v)[0][0],v,len(v.edges))
    prev_c=v.cordinates[0]
  #  for e in v.edges:
  #      print(e.atoms[0],e.atoms[1])
    for c in v.cordinates:
        #plt.plot(alpha*c[0], alpha*c[1], 'ro')
        if(abs(prev_c[0]-c[0])>10e-7 or abs(prev_c[1]-c[1])>10e-7 ):
            if(max_r<(abs(prev_c[0]-c[0])/abs(prev_c[1]-c[1]))):
                max_r=(abs(prev_c[0]-c[0])/abs(prev_c[1]-c[1]))
            if(min_r>(abs(prev_c[0]-c[0])/abs(prev_c[1]-c[1]))):
                min_r=(abs(prev_c[0]-c[0])/abs(prev_c[1]-c[1]))          
        prev_c=c
tol=10e-2
F1=0.
F1x=0.
F1y=0.
index1=0
F2=0.
F2x=0.
F2y=0.
index2=0
for v in vertices_all:
  #  print(np.where( np.array(vertices_all) == v)[0][0],v,len(v.edges))
    prev_c=v.cordinates[0]
  #  for e in v.edges:
  #      print(e.atoms[0],e.atoms[1])
    for c in v.cordinates:
        #plt.plot(alpha*c[0], alpha*c[1], 'co')
        if(abs(prev_c[0]-c[0])>10e-7 or abs(prev_c[1]-c[1])>10e-7 ):
            if(max_r - tol < abs(prev_c[0]-c[0])/abs(prev_c[1]-c[1])   and abs(prev_c[0]-c[0])/abs(prev_c[1]-c[1]) < max_r+tol):# abs(prev_c[1]-c[1])>10e-3 ):
                #print(abs(prev_c[0]-c[0]),abs(prev_c[1]-c[1]))
                #print(prev_c[0],prev_c[1],-alpha*(prev_c[0]-c[0]),-alpha*(prev_c[1]-c[1]))
                #ax.arrow(alpha*prev_c[0],alpha*prev_c[1],-alpha*(prev_c[0]-c[0]),-alpha*(prev_c[1]-c[1]),color='g',alpha=0.7)
                F1=F1+((prev_c[0]-c[0])**2+(prev_c[1]-c[1])**2)**0.5
                F1x=F1x+abs(prev_c[0]-c[0])
                F1y=F1y+abs(prev_c[1]-c[1])
                index1=index1+1
                #ax.plot(alpha*c[0], alpha*c[1], 'bo')
            elif (min_r - tol < abs(prev_c[0]-c[0])/abs(prev_c[1]-c[1])   and abs(prev_c[0]-c[0])/abs(prev_c[1]-c[1]) < min_r+tol):
                #ax.arrow(alpha*prev_c[0],alpha*prev_c[1],-alpha*(prev_c[0]-c[0]),-alpha*(prev_c[1]-c[1]),color='m',alpha=0.7)
                #ax.plot(alpha*c[0], alpha*c[1], 'go')
                F2=F2+((prev_c[0]-c[0])**2+(prev_c[1]-c[1])**2)**0.5
                F2x=F2x+abs(prev_c[0]-c[0])
                F2y=F2y+abs(prev_c[1]-c[1])
                index2=index2+1
            #else: 
                #ax.plot(alpha*c[0], alpha*c[1], 'ro')
        prev_c=c
F1x=F1x/index1
F1y=F1y/index1

F2x=F2x/index2
F2y=F2y/index2

theta=np.arctan(-F1y/F1x)
theta=-1.*theta
#theta=0
print(theta)
#theta=0.
for v in vertices_all:
  #  print(np.where( np.array(vertices_all) == v)[0][0],v,len(v.edges))
    #prev_c=v.cordinates[0]
  #  for e in v.edges:
  #      print(e.atoms[0],e.atoms[1])
    for c in v.cordinates:
        nC=[]
        nC.append(c[0]*np.cos(theta)-c[1]*np.sin(theta))
        nC.append(c[0]*np.sin(theta)+c[1]*np.cos(theta))
        #vertices_dat_ar.write(str(nC[0])+"\t"+str(nC[1])+"\n")
        vertices_dat.write(str(nC[0])+"\t"+str(nC[1])+"\n")
        #print(str(nC[0])+"\t"+str(nC[1])+" after_rot\n")
        #print(str(c[0])+"\t"+str(c[1])+"\n")
        break
#exit()

nF1x=F1x*np.cos(-theta)-F1y*np.sin(-theta)
nF1y=F1x*np.sin(-theta)+F1y*np.cos(-theta)

nF2x=F2x*np.cos(-theta)-F2y*np.sin(-theta)
nF2y=F2x*np.sin(-theta)+F2y*np.cos(-theta)

invariants_dat.write(sys.argv[3]+"\t"+str(F1/index1)+"\t"+str(F2/index2)+"\t"+str(nF1x)+"\t"+str(nF1y)+"\t"+str(nF2x)+"\t"+str(nF2y)+"\n")
exit()
network=open("network.dat","w")
for i in range (0,len(vertices_all)-1):
    for j in range (i+1,len(vertices_all)):
        for e in vertices_all[i].edges:
            for e_ in vertices_all[j].edges:
                #print('e1',e.atoms[0],e.atoms[1])
                #print('e2',e_.atoms[0],e_.atoms[1])
                if((e.atoms[0] == e_.atoms[0]) and (e.atoms[1] == e_.atoms[1])):
                    network.write(str(i)+"\t"+str(j)+"\n")
                    #print('**this pair',i,j,e.atoms[0],e.atoms[1])
write_edges = open("edges","w")
#fig, ax = plt.subplots(1, 1)
#ax.set_aspect(1)
for i in atoms:
    #i=1214
    #alpha=100
    for F in Force_tiles[i]:
    #print(([(F[0][0],F[0][1]),(F[1][0],F[1][1])]))
        t_f1x=F[0][0]
        t_f1y=F[0][1]
        t_f2x=F[1][0]
        t_f2y=F[1][1]
        F1x=t_f1x*np.cos(theta)-t_f1y*np.sin(theta)
        F1y=t_f1x*np.sin(theta)+t_f1y*np.cos(theta)

        F2x=t_f2x*np.cos(theta)-t_f2y*np.sin(theta)
        F2y=t_f2x*np.sin(theta)+t_f2y*np.cos(theta)
        write_edges.write(str(np.where( np.array(vertices_all) == F[3].vertices[0])[0][0])+"\t"+str(np.where( np.array(vertices_all) == F[3].vertices[1])[0][0])+"\t"+str(F1x)+"\t"+str(F1y)+"\t"+str(F2x)+"\t"+str(F2y)+"\n")
        #ax.arrow(alpha*F[0][0],alpha*F[0][1],alpha*F[1][0]-alpha*F[0][0],alpha*F[1][1]-alpha*F[0][1],color='C0')
#for F in Force_tiles[1012]:
    #print(([(F[0][0],F[0][1]),(F[1][0],F[1][1])]))
#    print("this0",F[3].vertices[0].cordinates[0][0],F[3].vertices[0].cordinates[0][1])
#    print("this1",F[3].vertices[1].cordinates[0][0],F[3].vertices[1].cordinates[0][1])
#    ax.annotate("0", xy=(alpha*F[3].vertices[0].cordinates[0][0],alpha*F[3].vertices[0].cordinates[0][1]),xytext=(alpha*F[3].vertices[0].cordinates[0][0]+0.1,alpha*F[3].vertices[0].cordinates[0][1]+0.1),arrowprops=dict(facecolor='black', shrink=0.05))
#    ax.annotate("1", xy=(alpha*F[3].vertices[1].cordinates[0][0],alpha*F[3].vertices[1].cordinates[0][1]),xytext=(alpha*F[3].vertices[1].cordinates[0][0]+0.1,alpha*F[3].vertices[1].cordinates[0][1]+0.1),arrowprops=dict(facecolor='red', shrink=0.05))
    #ax.annotate("1", xy=(F[3].vertices[1].cordinates[0],F[3].vertices[1].cordinates[1]))
#    plt.arrow(alpha*F[0][0],alpha*F[0][1],alpha*F[1][0]-alpha*F[0][0],alpha*F[1][1]-alpha*F[0][1],color='C4')
#for f in range (0,len(Forces)):
#    if(int(Forces[f][0])==i or int(Forces[f][1])==i):
#        if(len(Force_tiles[i])==0):
#            Force_tiles[i].append([[0.,0.],[Forces[f][3],Forces[f][4]]])
#        else:
#            last=len(Force_tiles[i])
#            prev_edge=Force_tiles[i][last-1]
#            #print(last,prev_edge[1])
#            Force_tiles[i].append([prev_edge[1],[prev_edge[1][0]+Forces[f][3],prev_edge[1][1]+Forces[f][4]]])
#for F in Force_tiles[i]:
    #print(F)

#i=102
#alpha=50
#for F in Force_tiles[i]:
#    #print(([(F[0][0],F[0][1]),(F[1][0],F[1][1])]))
#    plt.arrow(alpha*F[0][0],alpha*F[0][1],alpha*F[1][0]-alpha*F[0][0],alpha*F[1][1]-alpha*F[0][1],color='C0')
#for F in Force_tiles[i]:
#    #print(([(F[0][0],F[0][1]),(F[1][0],F[1][1])]))
#    plt.arrow(alpha*F[0][0],alpha*F[0][1],alpha*F[1][0]-alpha*F[0][0],alpha*F[1][1]-alpha*F[0][1],color='C5')
#    break
#i=1176
#alpha=50
#for F in Force_tiles[i]:
#    #print(([(F[0][0],F[0][1]),(F[1][0],F[1][1])]))
#    plt.arrow(alpha*F[0][0],alpha*F[0][1],alpha*F[1][0]-alpha*F[0][0],alpha*F[1][1]-alpha*F[0][1],color='C0')
#    #edges_to_draw.append([(F[0][0],F[0][1]),(F[1][0],F[1][1])])
#lc = mc.LineCollection(edges_to_draw,color=['r'])
#ax.add_collection(lc)
#plt.plot()
#ax.autoscale()
#plt.savefig("FTN.pdf")
#plt.show()

            
            #print(int(Forces[f][0]),int(Forces[f][1]))


