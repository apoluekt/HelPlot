import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from scipy.spatial.transform import Rotation
from mpl_toolkits.mplot3d import proj3d

# Some predefined arrays
zero = np.array([0, 0, 0], dtype=np.float64)

xaxis = np.array([1, 0, 0], dtype=np.float64)
yaxis = np.array([0, 1, 0], dtype=np.float64)
zaxis = np.array([0, 0, 1], dtype=np.float64)

xyplane = np.array([[-1, -1, 0], [-1, 1, 0], [1, 1, 0],
                   [1, -1, 0]], dtype=np.float64)
xzplane = np.array([[-1, 0, -1], [-1, 0, 1], [1, 0, 1],
                   [1, 0, -1]], dtype=np.float64)
yzplane = np.array([[0, -1, -1], [0, -1, 1], [0, 1, 1],
                   [0, 1, -1]], dtype=np.float64)


class ArrayBase:
    """
      Base class for types defined by a numpy array of shape (M, 3), 
      where M is arbitrary and second dimension corresponds to spatial coordinates.
      Implements rotations, shifts and scaling. 
    """

    def rotate(self, axis, angle):
        """
          Rotate the object by 'angle' degrees around 'axis'. 
          Returns the rotated object. Does not modify self. 
        """
        rot = Rotation.from_rotvec(np.radians(angle)*axis)
        return self.__class__(rot.apply(self.arr), **self.kwargs)

    def shift(self, vect):
        """
          Shift the object by 'vect'. 
          Returns the shifted object. Does not modify self. 
        """
        return self.__class__(self.arr + vect, **self.kwargs)

    def scale(self, fact):
        """
          Scale the object by the factor 'fact' (either scalar or 3-vector). 
          Returns the scaled object. Does not modify the self. 
        """
        return self.__class__(self.arr*fact, **self.kwargs)


class Plane(ArrayBase):
    """
      Plane in 3D defined by four points. Is represented by a rectangle. 
    """

    def __init__(self, descr="xy", **kwargs):
        """
          Constructor for the plane object. 'descr' is one of 
            - String 'xy', 'xy' or 'yz': defines a plane positioned at zero 
              represented by a 2x2 rectangle in the orientation given by `descr`
            - 2D numpy array of shape (M, 3), where M is the number of points 
              (typically 4 for the rectangular representation of a plane)
          Optionally, '**kwargs' can be provided and passed on to draw method
          (in this case, 'axis3d.plot'). 
        """
        if isinstance(descr, str):
            if descr == "xy":
                self.arr = xyplane
            elif descr == "xz":
                self.arr = xzplane
            elif descr == "yz":
                self.arr = yzplane
        else:
            self.arr = descr
        self.kwargs = kwargs

    def draw(self, ax):
        """
          Draw the rectangle (or any other representation) using triangulation. 
        """
        ax.plot_trisurf(self.arr[:, 0], self.arr[:, 1],
                        self.arr[:, 2], **self.kwargs)


class Angle:
    """
      Angle between lines or planes represented by one or several arcs. 
    """

    def __init__(self, origin, angle, radius, norm=None, start=None, **kwargs):
        """
          Constructor for the angle. Two patterns are recognised: 
            * If 'origin' is a string: 
              - 'origin' is one of 'xy', 'xz' or 'yz' that gives the orientation of the plane 
                in which the angle is defined
              - 'norm' and 'start' are ignored. 
            * If 'origin' is a numpy array: 
              - 'origin' is the vector of coordinates of the vertex
              - 'norm' is the unit normal to the plane in which the angle is defined
              - 'start' is the unit vector from which the angle will be counted
          And in both cases 
            - 'angle' is the angle in degrees
            - 'radius' is the radius of a single arc (if float) or several arcs 
              (if a list or tuple of floats)
          Optionally, '**kwargs' can be provided and passed on to draw method
          (in this case, 'axis3d.plot_trisurf'). 
        """
        if isinstance(origin, str):
            if origin == "xy":
                self.norm = zaxis
                self.start = xaxis
            elif origin == "xz":
                self.norm = -yaxis
                self.start = xaxis
            elif origin == "yz":
                self.norm = xaxis
                self.start = yaxis
            self.origin = zero
        else:
            self.origin = origin
            self.norm = norm
            self.start = start
        self.angle = angle
        self.radius = radius
        self.kwargs = kwargs

    def rotate(self, axis, angle):
        """
          Rotate the object by 'angle' degrees around 'axis'. 
          Returns the rotated object. Does not modify self. 
        """
        rot = Rotation.from_rotvec(np.radians(angle)*axis)
        return Angle(rot.apply(self.origin), self.angle, self.radius, rot.apply(self.norm), rot.apply(self.start), **self.kwargs)

    def shift(self, vect):
        """
          Shift the object by 'vect'. 
          Returns the shifted object. Does not modify self. 
        """
        return Angle(self.origin + vect, self.angle, self.radius, self.norm, self.start, **self.kwargs)

    def scale(self, fact):
        """
          Scale the object by the factor 'fact' (either scalar or 3-vector). 
          Returns the scaled object. Does not modify the self. 
        """
        return Angle(self.origin, self.angle, self.radius*fact, self.norm, self.start, **self.kwargs)

    def draw(self, ax):
        """
          Draw the Angle object
        """
        arc_resolution = 30
        u = self.start
        v = np.cross(self.norm, u)
        angles = np.linspace(0., np.radians(self.angle), arc_resolution)
        radius = self.radius if type(self.radius) in [
            list, tuple] else [self.radius]
        for r in radius:
            arc_points = self.origin + r * \
                (np.outer(np.cos(angles), u) + np.outer(np.sin(angles), v))
            ax.plot(arc_points[:, 0], arc_points[:, 1],
                    arc_points[:, 2], **self.kwargs)


class Arrow3D(FancyArrowPatch):
    """
      Auxiliary class for drawing the arrow in 3D. 
    """

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


class Line(ArrayBase):
    """
      Line represented by two points in space
    """

    def __init__(self, descr, **kwargs):
        """
          Constructor for the line. Two patterns are recognised: 
            * If 'descr' is the string, one of 'x', 'y', 'z', '-x', '-y', '-z': 
              - Line segment starting at zero and of unit length along the axis given by 'descr'. 
            * If 'descr' is the numpy array of shape (2,3): line between two arbitrary points. 
          Optionally, '**kwargs' can be provided and passed on to draw method
          (in this case, 'axis3d.plot'). 
        """
        if isinstance(descr, str):
            if descr == 'x':
                self.arr = np.stack([zero, xaxis], axis=0)
            elif descr == 'y':
                self.arr = np.stack([zero, yaxis], axis=0)
            elif descr == 'z':
                self.arr = np.stack([zero, zaxis], axis=0)
            elif descr == '-x':
                self.arr = np.stack([zero, -xaxis], axis=0)
            elif descr == '-y':
                self.arr = np.stack([zero, -yaxis], axis=0)
            elif descr == '-z':
                self.arr = np.stack([zero, -zaxis], axis=0)
        else:
            self.arr = descr
        self.kwargs = kwargs

    def draw(self, ax):
        """
          Draw the line
        """
        ax.plot([self.arr[0, 0], self.arr[1, 0]],
                [self.arr[0, 1], self.arr[1, 1]],
                [self.arr[0, 2], self.arr[1, 2]],
                **self.kwargs)


class Arrow(Line):
    """
      Arrow represented by two points in space ('from'->'to'). 
      Uses 'Line' as base class and the same constructor. 
    """

    def draw(self, ax):
        """
          Draw the arrow. 
        """
        arrow = Arrow3D([self.arr[0, 0], self.arr[1, 0]],
                        [self.arr[0, 1], self.arr[1, 1]],
                        [self.arr[0, 2], self.arr[1, 2]],
                        arrowstyle='-|>', mutation_scale=20, **self.kwargs)
        ax.add_artist(arrow)


class Point(ArrayBase):
    """
      Point in space. 
    """

    def __init__(self, arr=zero, **kwargs):
        """
          Constructor. 
          'arr' is the array of 3 elements representing the coordinates of the point. 
          Optionally, '**kwargs' can be provided and passed on to draw method
          (in this case, 'axis3d.scatter'). 
        """
        self.arr = arr
        self.kwargs = kwargs

    def draw(self, ax):
        """
          Draw the point. 
        """
        ax.scatter(self.arr[0], self.arr[1], self.arr[2], **self.kwargs)


class Text:
    """
      Text label bound to a point in 3D space. 
    """

    def __init__(self, text, coord, **kwargs):
        """
          Constructor for Text object. 
          - 'text' is the text label (string). 
          - 'coord' is the 3-element array of coordinates in space
          Optionally, '**kwargs' can be provided and passed on to draw method
          (in this case, 'axis3d.text'). 
        """
        self.text = text
        self.arr = coord
        self.kwargs = kwargs

    def rotate(self, axis, angle):
        """
          Rotate the object by 'angle' degrees around 'axis'. 
          Returns the rotated object. Does not modify self. 
        """
        rot = Rotation.from_rotvec(np.radians(angle)*axis)
        return Text(self.text, rot.apply(self.arr), **self.kwargs)

    def shift(self, vect):
        """
          Shift the object by 'vect'. 
          Returns the shifted object. Does not modify self. 
        """
        return Text(self.text, self.arr + vect, **self.kwargs)

    def scale(self, fact):
        """
          Scale the object by the factor 'fact' (either scalar or 3-vector). 
          Returns the scaled object. Does not modify the self. 
        """
        return Text(self.text, self.arr*fact, **self.kwargs)

    def draw(self, ax):
        """
          Draw the text
        """
        ax.text(self.arr[0], self.arr[1],
                self.arr[2], self.text, **self.kwargs)


class Compound:
    """
      Compound can merge several objects such that they can be rotated, 
      shifted, scaled and drawn together. 
    """

    def __init__(self, *elements):
        """
          Constructor for coumpound object. Takes objects to be combined as arguments. 
        """
        self.elements = elements

    def rotate(self, axis, angle):
        """
          Rotate the object by 'angle' degrees around 'axis'. 
          Returns the rotated object. Does not modify self. 
        """
        return Compound(*[i.rotate(axis, angle) for i in self.elements])

    def shift(self, vect):
        """
          Shift the object by 'vect'. 
          Returns the shifted object. Does not modify self. 
        """
        return Compound(*[i.shift(vect) for i in self.elements])

    def scale(self, factor):
        """
          Scale the object by the factor 'fact' (either scalar or 3-vector). 
          Returns the scaled object. Does not modify the self. 
        """
        return Compound(*[i.scale(factor) for i in self.elements])

    def draw(self, ax):
        """
          Draw the compound object. 
        """
        for i in self.elements:
            i.draw(ax)
