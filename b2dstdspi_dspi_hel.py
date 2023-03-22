import numpy as np
import matplotlib.pyplot as plt
from helplot import *

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=14)

# Create 3D plot axes
fig = plt.figure(figsize=(3.1, 3.1))
ax = fig.add_subplot(111, projection='3d')
fig.subplots_adjust(bottom=0., left=0., right=1., top=1.)

# Helicity angles values for this illustration
theta_d = 70
theta_l = 80
chi = 60

# Construct the plot
Compound(
    Compound(
        Plane("xy", color='r', alpha=0.3).scale(0.7+0.3*yaxis),
        Compound(
            Arrow("x", color='k'),
            Text("$D_s^+$", 1.05*xaxis, color='k')).rotate(zaxis, theta_d),
        Compound(
            Arrow("x", color='k'),
            Text(r"$\pi^+$", 1.25*xaxis, color='k')).rotate(zaxis, 180+theta_d),
        Angle("xy", theta_d, (0.25, 0.28), color='k'),
        Text(r"$\theta_{D_{s}}^{c\bar{s}}$", 0.35*xaxis,
             color='k').rotate(zaxis, 0.4*theta_d),
        Point(marker='o', color='r')
    ).shift(0.7*xaxis),
    Compound(
        Plane("xy", color='b', alpha=0.3).scale(0.7+0.3*yaxis),
        Compound(
            Arrow("-x", color='k'),
            Text("$\overline{D}{}^{0}$", -1.3*xaxis, color='k')).rotate(zaxis, theta_l),
        Compound(
            Arrow("-x", color='k'),
            Text(r"$\pi^{-}$", -1.1*xaxis, color='k')).rotate(zaxis, 180+theta_l),
        Angle("xy", theta_l, (0.24, 0.28, 0.32), color='k').rotate(zaxis, 180),
        Text(r"$\theta_D^{c\bar{s}}$", 0.70*xaxis,
             color='k').rotate(zaxis, 180 + theta_l/2.),
        Point(marker='o', color='b')
    ).rotate(xaxis, chi).shift(-0.7*xaxis),
    Line("x", color="k", linestyle="--",
         linewidth=1).shift(-0.5*xaxis).scale(3.6),
    Angle("yz", chi, 0.5, color='k'),
    Text(r"$\phi_D^{c\bar{s}}$", 0.6*yaxis, color='k').rotate(xaxis, 0.7*chi),
    Point(marker='o', color='g'),
    Arrow("x", color='k').scale(0.7),
    Arrow("-x", color='k').scale(0.7),
    Text(r"$D^{*-}$", -0.6*xaxis+0.1*zaxis, color='k'),
    Text(r"$T_{c\bar{s}}^{++}$", 0.5*xaxis+0.1*zaxis, color='k'),
    Text(r"$B^+$", -0.2*zaxis-0.2*yaxis, color='k'),
).draw(ax)

scale = 0.9

ax.set_xlim([-1.3*scale, 1.3*scale])
ax.set_ylim([-scale, scale])
ax.set_zlim([-scale, scale])
ax.axis('off')

plt.show()
fig.savefig("b2dstdspi_dspi_hel.pdf")
