from numpy import sin,cos,arctan,pi,arange,sqrt
import matplotlib.pyplot as plt

#import four_bar as bar

plt.rcParams['figure.figsize'] = (11,7) ## Altera tamanho da imagem

def cart2pol(x, y):
    r_calculo = sqrt(x**2 + y**2)
    tet_calculo = arctan(y, x)
    return(r_calculo, tet_calculo)

def pol2cart(r_calculo, tet_calculo):
    x = r_calculo * cos(tet_calculo)
    y = r_calculo * sin(tet_calculo)
    return(x, y)

## ----- Dados de entrada do programa ----- ##

Wm = 1 ## 1rpm // 1rpm = 1rp60s//Rotação Mesa 
Wc = 1535 ## 1535 rpm //Rotação Cabeçote
Wf = 11.7 ## 11.7 rpm //Rotação motor de oscilação

Dm = 127.5*2 ## 350 mm //Diametro médio da mesa
A = 34 ## 34 mm //Amplitude da oscilação
Rho = -18 ## -13 graus

Da = 77 ## 77 normal e 74 canetas //Diametro médio do abrasivo

tamanho_axial = 15 # mm //Tamanho do abrasivo na direção axial
tamanho_radial = 15 #19 # mm //Tamanho do abrasivo na direção radial

tile_length = 450

## Tempos e intervalos executados 
inicio = 0
fim = 60
interv = 0.001

## ----- Cálculos iniciais ----- ##

tt = arange(inicio,fim,interv) ## Matriz de tempo
f =  Wf/60 # s^-1 //Frequencia de oscilação
rm = Dm/2
wm = Wm*pi/30
wc = Wc*pi/30
ra = Da/2
rho = Rho*(pi/180)

abra=[0 ,pi] ## Usado para calcular o segundo abrasivo

l1 = arange(-tamanho_axial/2,tamanho_axial/2 + 0.01,tamanho_axial/4) ## Distancia Axial
l2 = arange(-tamanho_radial/2,tamanho_radial/2 + 0.01,tamanho_radial/4) ## Distancia Radial

## ----- Cálculo da trajetória ----- ##
def traj():

    #new_T4 = bar.four_bar(tt)
    #new_T4 = sin(2*pi*f*tt)
    
    X = rm*cos(-wm*tt+pi) + (-A*sin(2*pi*f*tt))*cos(-wm*tt+pi)*cos(rho) - (-A*sin(2*pi*f*tt))*sin(-wm*tt+pi)*sin(rho) + ra*cos(wc*tt) 
    Y = rm*sin(-wm*tt+pi) + (-A*sin(2*pi*f*tt))*cos(-wm*tt+pi)*sin(rho) + (-A*sin(2*pi*f*tt))*sin(-wm*tt+pi)*cos(rho) + ra*sin(wc*tt)
    
    plt.plot(X,Y,linewidth = 0.2)
    plt.gca().set_aspect('equal', adjustable='box') ## x = y scale
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    #plt.title('Trajetória do ponto central de abrasivo')
    plt.xlim(-tile_length/2, tile_length/2)
    plt.ylim(-tile_length/2, tile_length/2*0)
    #plt.ylim(0, tile_length/2)
    #plt.legend(['Rotação da mesa: '+str(Wm)+' rpm' +'\nRotação do cabeçote: '+str(Wc)+' rpm'+'\nFrequência de Oscilação: '+str(round(f,3))+' Hz'], loc= 4)
    plt.show()
        
## ----- Cálculo da distribuição ----- ##
 
def dist():
    Xa=[] ## Matrizes que armazenam os pontos
    Ya=[]       
      
    for t in tt:
        for abr in abra:
            for n in l1:
                for m in l2:
                    X2 = rm*cos(-wm*t+pi) + (-A*sin(2*pi*f*t))*cos(-wm*t+pi)*cos(rho) - (-A*sin(2*pi*f*t))*sin(-wm*t+pi)*sin(rho) + ra*cos((wc*t)+abr) + n*cos((wc*t)+abr) + m*cos((wc*t)+abr+pi/2) 
                    Y2 = rm*sin(-wm*t+pi) + (-A*sin(2*pi*f*t))*cos(-wm*t+pi)*sin(rho) + (-A*sin(2*pi*f*t))*sin(-wm*t+pi)*cos(rho) + ra*sin((wc*t)+abr) + n*sin((wc*t)+abr) + m*sin((wc*t)+abr+pi/2)
                    Xa.append(X2)
                    Ya.append(Y2)
                    
    fig,ax = plt.subplots()
    #plt.title('Contato sobre a placa')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.hist2d(Xa, Ya, bins=(90, 90), cmap=plt.cm.jet, range = [[-tile_length/2, tile_length/2],[-tile_length/2, tile_length/2]])
    cb = plt.colorbar(label='Número de contatos',)  
    plt.legend(['Rotação da mesa: '+str(Wm)+' rpm' +'\nRotação do cabeçote: '+str(Wc)+' rpm'+'\nFrequência de oscilação: '+str(round(f,2))+' Hz'], loc= 4)
    plt.show()
    return Xa,Ya
          
    #cb.set_ticks([0, 2000, 4000, 6000])  ###manual
    #cb.set_ticklabels(['0%', '25%', '75%', '100%'])
    
## ----- Cálculo da velocidade ----- ##
def veloc():
    VX = 2*pi*A*f*np.cos(2*pi*f*tt)*np.cos(wm*tt) - ra*wc*np.sin(wc*tt) - wm*(A*np.sin(2*pi*f*tt)+rm)*np.sin(wm*tt)
    VY = -2*pi*A*f*np.cos(2*pi*f*tt)*np.sin(wm*tt) + ra*wc*np.cos(wc*tt) + wm*(-A*np.sin(2*pi*f*tt)-rm)*np.cos(wm*tt)
    V = np.sqrt(VX**2+VY**2)
    
    plt.plot(tt,V)
    plt.xlabel('t [s]')
    plt.ylabel('V [mm/s]')
    
    mediav = sum(V)/len(V)
    print('Média de velocidade do abrasivo: '+ str(mediav))
    
    
##plt.savefig('velocidade.svg', format='svg', dpi=1000) ##Save the file

def abras(n):
    Xa=[] 
    Ya=[] 
    t = tt[n]
    for abr in abra:
        for n in l1:
            for m in l2: 
                X2 = rm*cos(-wm*t+pi) + (-A*sin(2*pi*f*t))*cos(-wm*t+pi)*cos(-rho*(pi/180)) - (-A*sin(2*pi*f*t))*sin(-wm*t+pi)*sin(-rho*(pi/180)) + ra*cos((wc*t)+abr) + n*cos((wc*t)+abr) + m*cos((wc*t)+abr+pi/2) 
                Y2 = rm*sin(-wm*t+pi) + (-A*sin(2*pi*f*t))*cos(-wm*t+pi)*sin(-rho*(pi/180)) + (-A*sin(2*pi*f*t))*sin(-wm*t+pi)*cos(-rho*(pi/180)) + ra*sin((wc*t)+abr) + n*sin((wc*t)+abr) + m*sin((wc*t)+abr+pi/2)
                Xa.append(X2)
                Ya.append(Y2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot (Xa,Ya,'o')

traj()
#dist()
'''
for k in range(100,102):
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(color='black', linestyle='-', linewidth=0.5)
    plt.xticks(arange(-180, 80, step=5))
    plt.yticks(arange(-180, 80, step=5))
    abras(k)
    
'''
