import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#Resistencia de la bobina
Rl=150
#Inductancia de la bobina
L=220e-6
#Resistencia de Gate
Rg=100
#Tensión del generador de gate
Vgg=15
#
Vd=50

#Tensión máxima que soporta el switch
Vswmax=Vd
#Corriente de carga  (Me da 0.3333A)
Io=Vswmax/Rl
#Para una Io de 0.333A
Vgsio=4.1
#Capacitor entre gate y source 1
Cgd1cgs=650e-12
#Capacitor entre gate y source 2
Cgd2cgs=1150e-12
#Tensión de threshold
Vgsth=4
#Constante de carga 1
tau1=Rg*Cgd1cgs
#Constante de carga 2
tau2=Rg*Cgd2cgs
#
t1=-tau2*np.log(Vgsio/Vgg)
print("Tdoff es",t1)


# td=-tau1*np.log(1-Vgsth/Vgg)
# #
# tri=t1-td
# print("Tiempo de rise de corriente es",tri)

#Variación de carga del capacitor mientras vgs queda constante
deltaQ=5.5e-9
#tiempo en el que vgs se mantiene constante
trv=deltaQ/(Vgsio/Rg)
print("Tiempo de rise de tension es",trv)

#tfi
tfi=-tau1*np.log(Vgsth/Vgsio)
print("Tiempo de fall de corriente es",tfi)

time_len=800e-9
samples=5000
t=np.linspace(start=0,stop=time_len,num=samples)
deltat=time_len/samples

#VGS apagado
p1=Vgg*np.exp(-t[0:int(t1/deltat)]/tau2)
p2=np.ones(int((t1+trv)/deltat)-int(t1/deltat)-1)*Vgsio
p3=Vgsio*np.exp(-t[:len(t)-int((t1+trv)/deltat)]/tau1)
Vgs=np.append(p1,p2)
Vgs=np.append(Vgs,p3)
#Ig apagado
p1=-Vgg/Rg*np.exp(-t[0:int(t1/deltat)]/tau2)
p2=p1[-1]*np.ones(int((t1+trv)/deltat)-int(t1/deltat)-1)
p3=p2[0]*(np.exp(-t[:len(t)-int((t1+trv)/deltat)]/tau1))
Ig=np.append(p1,p2)
Ig=np.append(Ig,p3)
#Id apagado
p1=Io*np.ones(int((t1+trv)/deltat))
p2=Io-Io/(tfi)*t[0:len(t)-int((t1+trv)/deltat)-1]
Id=np.append(p1,p2)
#VDS apagado
p1=np.zeros(int(t1/deltat))
p2=Vswmax/trv*t[0:int(trv/deltat)]
p3=Vswmax*np.ones(len(t)-int((t1+trv)/deltat)-1)
Vds=np.append(p1,p2)
Vds=np.append(Vds,p3)



#L
df = pd.read_csv('off.csv',skiprows=1, names=['t', 'V(drain)',"V(gate)", "I(R1)", "Id(M1)"])
t_sim=[float(i) for i in df["t"]]
Vds_sim=[float(i) for i in df["V(drain)"]]
Vgs_sim=[float(i) for i in df["V(gate)"]]
Id_sim=[float(i) for i in df["Id(M1)"]]
Ig_sim=[float(i) for i in df["I(R1)"]]

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


#Para VGS y IG

fig, host = plt.subplots()
fig.subplots_adjust(right=0.75)

par1 = host.twinx()
host.grid(True)
p1, = host.plot(t[:-1], Vgs, '#b576ad', label="V_gs teórico")
p2, = host.plot(t_sim,Vgs_sim,"#e04644",label="V_gs simulado")
p3, = par1.plot(t[:-1], Ig, "#a1d046", label="I_g teórico")
p4, = par1.plot(t_sim,Ig_sim,"#7ccce5",label="I_g simulado")
#Fijo limites en X
host.set_xlim(0, time_len)
#Fijo limites en Y para el primer eje
host.set_ylim(0, 15)
#Fijo limites en Y para el segundo eje
par1.set_ylim(-.25, .20)

host.set_xlabel("Tiempo [s]")
host.set_ylabel("Tensión [V]")
par1.set_ylabel("Corriente [A]")

host.yaxis.label.set_color("black")
par1.yaxis.label.set_color("black")
tkw = dict(size=4, width=1.5)
host.tick_params(axis='y', color="black", **tkw)
par1.tick_params(axis='y', color="black", **tkw)

host.tick_params(axis='x', **tkw)

lines = [p1, p2, p3, p4]

host.legend(lines, [l.get_label() for l in lines])
# plt.grid(True)
plt.show()



#PARA VDS y ID

fig, host = plt.subplots()
fig.subplots_adjust(right=0.75)

par1 = host.twinx()
host.grid(True)
p1, = host.plot(t[:-1], Vds, '#b576ad', label="V_ds teórico")
p2, = host.plot(t_sim,Vds_sim,"#e04644",label="V_ds simulado")
p3, = par1.plot(t[:-1], Id, "#a1d046", label="I_d teórico")
p4, = par1.plot(t_sim,Id_sim,"#7ccce5",label="I_d simulado")

#Fijo limites en X
host.set_xlim(0, time_len)
#Fijo limites en Y para el primer eje
host.set_ylim(0, 52)
#Fijo limites en Y para el segundo eje
par1.set_ylim(0, 500e-3)

host.set_xlabel("Tiempo [s]")
host.set_ylabel("Tensión [V]")
par1.set_ylabel("Corriente [A]")

host.yaxis.label.set_color("black")
par1.yaxis.label.set_color("black")
tkw = dict(size=4, width=1.5)
host.tick_params(axis='y', colors="black", **tkw)
par1.tick_params(axis='y', colors="black", **tkw)

host.tick_params(axis='x', **tkw)

lines = [p1, p2, p3, p4]

host.legend(lines, [l.get_label() for l in lines])
plt.show()