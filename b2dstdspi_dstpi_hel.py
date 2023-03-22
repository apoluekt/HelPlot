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
        Plane("xy", color='r', alpha=0.3).scale(
            0.7+0.6*yaxis).shift(-0.6*yaxis+0.2*xaxis),
        Compound(
            Arrow("x", color='k'),
            Text(r"$\pi^+$", 1.*xaxis+0.1*yaxis, color='k')),
        Compound(
            Arrow("-x", color='k').scale(1.2),
            Text(r"$D^{*-}$", -1.15*xaxis+0.15*yaxis, color='k')),
        Compound(
            Arrow("-x", color='k'),
            Text("$D_s^+$", -1.2*xaxis, color='k'),
            Arrow("x", color='k'),
            Text("$D^{**0}$", 0.4*xaxis-0.1*yaxis, color='k'),
            Point(marker='o', color='g'),
            Text("$B^+$", zero, color='k').shift(-0.1*yaxis),
            Line("x", color="k", linestyle="--", linewidth=1).scale(2.),
        ).shift(-xaxis).rotate(zaxis, 180-theta_d),
        Angle("xy", theta_d, (0.25, 0.28), color='k').rotate(
            zaxis, 180-theta_d),
        Text(r"$\theta_{D^*}$", 0.5*xaxis,
             color='k').rotate(zaxis, 180-0.4*theta_d),
        Point(marker='o', color='r')
    ).shift(0.5*xaxis),
    Compound(
        Plane("xy", color='b', alpha=0.3).scale(0.7+0.3*yaxis),
        Compound(
            Arrow("-x", color='k'),
            Text("$\overline{D}{}^{0}$", -1.3*xaxis+0.2*yaxis, color='k')).rotate(zaxis, theta_l),
        Compound(
            Arrow("-x", color='k'),
            Text(r"$\pi^{-}$", -1.1*xaxis, color='k')).rotate(zaxis, 180+theta_l),
        Angle("xy", theta_l, (0.24, 0.28, 0.32), color='k').rotate(zaxis, 180),
        Text(r"$\theta_D$", 0.7*xaxis, color='k').rotate(zaxis, 180 + theta_l/2.),
        Point(marker='o', color='b')
    ).rotate(xaxis, chi).shift(-0.7*xaxis),
    Line("x", color="k", linestyle="--",
         linewidth=1).shift(-0.5*xaxis).scale(3.6),
    Angle("yz", chi, 0.6, color='k'),
    Text(r"$\phi_D$", 0.7*yaxis, color='k').rotate(xaxis, 0.6*chi)
).draw(ax)

scale = 0.9

ax.set_xlim([-1.3*scale, 1.3*scale])
ax.set_ylim([-scale, scale])
ax.set_zlim([-scale, scale])
ax.axis('off')

plt.show()
fig.savefig("b2dstdspi_dstpi_hel.pdf")
