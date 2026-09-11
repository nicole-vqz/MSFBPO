"""
Práctica 0: Mecánica pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Nicole Vazquez Alvear
Número de control: C20210923
Correo institucional: lC20210923@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt

# Datos generales de la simulacion
x0,t0,tend,dt,w,h=0,0,10,1E-3,7,3.5
N=round(tend/dt)+1
t=np.linspace(t0,tend,N)
u1=np.ones(N)
u2=np.zeros(N); u2[round(1/dt):round(2/dt)]=1
u3=t/tend
u4=np.sin(m.pi/2*t)
u=np.column_stack((u1,u2,u3,u4))
signals=['step','impulse','ramp','sinusoidal']

# Componentes del circuito RLC
R,L,C=10E3,47E-6,100E-6
num=[1]
den=[L*C,R*C,1]
sys=ctrl.tf(num,den)
print(f"Funcion de transferencia: {sys}\n")

# Polos del sistema
poles= np.roots(den)
print(f"Polos del sistema: L1= {poles[0]:.3E}, L2= {poles[1]:.3E}\n")

# Componentes del controlador
kP,kI,kD=289.661,7061.510,0.391
Cr=1E-6
Re=1/(Cr*kI)
Rr=kP*Re
Ce=kD/Rr
numPID=[Re*Rr*Ce*Cr,Re*Ce+Rr*Cr,1]
denPID=[Re*Cr,0]
PID=ctrl.tf(numPID,denPID)
print(f"Capacitancia Cr: {Cr} Faradios\n")
print(f"Resistencia Re: {Re} Ohms\n")
print(f"Resistencia Rr: {Rr} Ohms\n")
print(f"Capacitancia Ce: {Ce} Faradios\n")
print(f"Funcion de transferencia del controlador PID: {PID}\n")

# Sistema en lazo cerrado
sysPID=ctrl.feedback(ctrl.series(PID,sys),1,sign=-1)
print(f"Funcion de transferencia del sistema en lazo cerrado: {sysPID}\n")

# Colores 
clr1 = np.array([248, 178, 178])/255
clr2 = np.array([175, 113, 157])/255
clr3 = np.array([64, 61, 136])/255

# Funciones del sistema en lazo abierto y lazo cerrado
def openloop(t,sys,u):
    _,PAu = ctrl.forced_response(sys,t,u,x0)
    return PAu

def closedloop(t,sysPID,u):
    _,PIDu = ctrl.forced_response(sysPID,t,u,x0)
    return PIDu

# Respuestas: Simulaciones numericas
for i in range(0,4):
    PAu = openloop(t,sys,u[:,i])
    PIDu = closedloop(t,sysPID,u[:,i])
    fg = plt.figure(i+1)
    fg.set_size_inches(w,h)
    plt.rcParams['font.size'] = 11
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.plot(t,u[:,i], '-', color = clr1,label='Pao(t)')
    plt.plot(t,PAu,'--',color=clr2,label='PA(t)')
    plt.plot(t,PIDu,':',linewidth=2.5,color=clr3,label='PID(t)')
    plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
    if i==0 or i==1 or i==2:
        plt.ylim(-0.1,1.2); plt.yticks(np.arange(-0.1,1.3,0.1))
    elif i ==3:
        plt.ylim(-1.2,1.2); plt.yticks(np.arange(-1.2,1.4,0.2))
    plt.xlabel('t[s]')
    plt.ylabel('Vi(t)[V]')
    plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=3, frameon=False)
    plt.show()
    fg.savefig(signals[i]+'python.pdf',bbox_inches='tight')