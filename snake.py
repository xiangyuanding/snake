# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 23:24:37 2022

@author:
"""

import time
import sys
import pygame
import random
class head:
    def __init__(self,x_p,y_p,next_node,skin,dire):
        
        self.x_p=x_p
        self.y_p=y_p
        self.p=[self.x_p,self.y_p]
        self.next_node=next_node
        self.skin=skin
        self.dire=dire
        self.pp=(self.x_p,self.y_p)
        self.rect=0
        
    def move(self,pos,speed):
        
        self.pp=(self.x_p,self.y_p)
        self.rect=self.skin.get_rect()
        
        if pos=="w":
            self.y_p=self.y_p-speed
        if pos=="a":
            self.x_p=self.x_p-speed
        if pos=="s":
            self.y_p=self.y_p+speed
        if pos=="d":
            self.x_p=self.x_p+speed

        self.rect=self.rect.move((self.x_p%size,self.y_p%size))
        
        window.blit(self.skin, self.rect)
        
        self.next_node.move()
        
    
class body:
    def __init__(self,x_p,y_p,next_node,prev_node,skin):
        
        self.x_p=x_p
        self.y_p=y_p
        self.p=[self.x_p,self.y_p]
        self.next_node=next_node
        self.prev_node=prev_node
        self.skin=skin
        self.pp=(x_p,y_p)
        
    def move(self):
        self.rect=self.skin.get_rect()
        self.pp=(self.x_p,self.y_p)
        self.x_p=self.prev_node.pp[0]
        self.y_p=self.prev_node.pp[1]
        self.rect=self.rect.move((self.x_p%size,self.y_p%size))
        window.blit(self.skin, self.rect)
        
        if self.next_node==0:
            pass
        else:
            self.next_node.move()

class food:
    def __init__(self,x_p,y_p,skin):
        self.x_p=x_p
        self.y_p=y_p
        self.skin=skin
        
def get_pos(head,pos_list):
    pos_list.append([head.x_p%size,head.y_p%size])
    if head.next_node!=0:
        return get_pos(head.next_node,pos_list)
    else:
        return pos_list
    
def check_c(head):
    pos_list=[]         
    if [head.x_p%size,head.y_p%size] in get_pos(head.next_node.next_node,pos_list):
        pygame.quit()
        sys.exit()

def spawn(fnum):
    skin2=pygame.image.load("./image.jpg").convert()
    skin2=pygame.transform.scale(skin2,(30,30))
    x=randlist[fnum][0]
    y=randlist[fnum][1]
    
    food1=food(x,y,skin2)
    window.blit(food1.skin,(food1.x_p,food1.y_p))
    return food1

def check_range(head,food1):
    if (head.x_p%size in range(food1.x_p-15, food1.x_p+15)) and (head.y_p%size in range(food1.y_p-15, food1.y_p+15)):
        return True
    else:
        return False
    
def add_node(head):
    tail=get_lastnode(head)
    newnode=body(0,0,0,tail,skin1)
    tail.next_node=newnode
    if tail.prev_node.x_p==tail.x_p:
        newnode.y_p=tail.y_p-(tail.prev_node.y_p-tail.y_p)
        newnode.x_p=tail.x_p
    else:
        newnode.x_p=tail.x_p-(tail.prev_node.x_p-tail.x_p)
        newnode.y_p=tail.y_p
    
    return newnode
    
def get_lastnode(head):
    if head.next_node!=0:
        return get_lastnode(head.next_node)
    else:
        return head
    

randlist=[]

for i in range(90):
    x=random.randint(50,850)
    y=random.randint(50,850)
    randlist.append((x,y))
    
size=900
pygame.init()
window=pygame.display.set_mode((size,size))
pygame.display.set_caption('eating human')
window.fill("white")

skin1=pygame.image.load("./image.jpg").convert()
skin1=pygame.transform.scale(skin1,(30,30))
s=head(200,200,0,skin1,"D")
window.blit(s.skin,s.p)
prevnd=s
for i in range(6):
    i=pygame.image.load("./image.jpg").convert()
    i=pygame.transform.scale(i,(30,30))
    i=body(prevnd.x_p+30,prevnd.y_p,0,prevnd,i)
    window.blit(i.skin,((i.x_p,i.y_p)))
    prevnd.next_node=i
    prevnd=i

numf=0

food1=spawn(numf)

dire="w"
pdire="w"
cdire="w"
diredict={"w":"s","s":"w","a":'d','d':"a"}
while True:
    check_c(s)
    time.sleep(0.2)
    event1=pygame.event.get()
    
    for event in event1:
        
        if event.type == pygame.QUIT:
            
            pygame.quit()
            
            sys.exit()
        if event.type==pygame.KEYDOWN:
            
            if event.key==pygame.K_w:
                dire='w'
            if event.key==pygame.K_a:
                dire='a'
            if event.key==pygame.K_s:
                dire='s'
            if event.key==pygame.K_d:
                dire='d'
            if dire!=diredict[pdire]:
                cdire=dire
    window.fill("white")
    s.move(cdire,30)
    pdire=cdire
    if check_range(s, food1):
        numf+=1
        food1=spawn(numf)
        newnode=add_node(s)
        window.blit(newnode.skin,(newnode.x_p%size,newnode.y_p%size))
        #print(newnode.x_p,newnode.y_p)
        #print(get_lastnode(s).x_p,get_lastnode(s).y_p)
    else:
        food1=spawn(numf)
    pygame.display.flip() 