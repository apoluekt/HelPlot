import numpy as np
import matplotlib.pyplot as plt
from helplot import *

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=14)

# Create 3D plot axes
fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(111, projection='3d')

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
            Text("$D^0$", 1.1*xaxis, color='k')).rotate(zaxis, theta_d),
        Compound(
            Arrow("x", color='k'),
            Text(r"$\pi^+$", 1.25*xaxis, color='k')).rotate(zaxis, 180+theta_d),
        Angle("xy", theta_d, (0.25, 0.28), color='k'),
        Text(r"$\theta_D$", 0.35*xaxis, color='k').rotate(zaxis, theta_d/2.),
        Point(marker='o')
    ).shift(0.7*xaxis),
    Compound(
        Plane("xy", color='b', alpha=0.3).scale(0.7+0.3*yaxis),
        Compound(
            Arrow("-x", color='k'),
            Text("$\mu^+$", -1.2*xaxis, color='k')).rotate(zaxis, theta_l),
        Compound(
            Arrow("-x", color='k'),
            Text(r"$\nu_{\mu}$", -1.1*xaxis, color='k')).rotate(zaxis, 180+theta_l),
        Angle("xy", theta_l, (0.24, 0.28, 0.32), color='k').rotate(zaxis, 180),
        Text(r"$\theta_{\ell}$", 0.60*xaxis,
             color='k').rotate(zaxis, 180 + theta_l/2.),
        Point(marker='o')
    ).rotate(xaxis, chi).shift(-0.7*xaxis),
    Line("x", color="k", linestyle="--").shift(-0.5*xaxis).scale(4.),
    Angle("yz", chi, 0.5, color='k'),
    Text(r"$\chi$", 0.7*yaxis, color='k').rotate(xaxis, chi/2.),
    Point(marker='o')
).draw(ax)

scale = 1.

ax.set_xlim([-scale, scale])
ax.set_ylim([-scale, scale])
ax.set_zlim([-scale, scale])
ax.axis('off')

plt.show()
fig.savefig("b2dstmunu_hel.pdf")
