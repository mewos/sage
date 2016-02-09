r"""
Coordinate Charts

The class :class:`Chart` implements coordinate charts on a topological
manifold over a topological field `K`. The subclass :class:`RealChart`
is devoted to the case `K=\RR`, for which the concept of coordinate
range is meaningful.

Transition maps between charts are implemented via the class
:class:`CoordChange`.

AUTHORS:

- Eric Gourgoulhon, Michal Bejger (2013-2015) : initial version
- Travis Scrimshaw (2015): review tweaks

REFERENCES:

- Chap. 2 of [Lee11]_ J.M. Lee: *Introduction to Topological Manifolds*,
  2nd ed., Springer (New York) (2011)

- Chap. 1 of [Lee13]_ J.M. Lee : *Introduction to Smooth Manifolds*,
  2nd ed., Springer (New York) (2013)
"""

#*****************************************************************************
#       Copyright (C) 2015 Eric Gourgoulhon <eric.gourgoulhon@obspm.fr>
#       Copyright (C) 2015 Michal Bejger <bejger@camk.edu.pl>
#       Copyright (C) 2015 Travis Scrimshaw <tscrimsh@umn.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.structure.sage_object import SageObject
from sage.structure.unique_representation import UniqueRepresentation
from sage.symbolic.ring import SR
from sage.rings.infinity import Infinity
from sage.misc.latex import latex

class Chart(UniqueRepresentation, SageObject):
    r"""
    Chart on a topological manifold.

    Given a topological manifold `M` of dimension `n` over a topological
    field `K`, a *chart* on `M` is a pair `(U, \varphi)`, where `U` is an
    open subset of `M` and `\varphi : U \rightarrow V \subset K^n` is a
    homeomorphism from `U` to an open subset `V` of `K^n`.

    The components `(x^1, \ldots, x^n)` of `\varphi`, defined by
    `\varphi(p) = (x^1(p), \ldots, x^n(p)) \in K^n` for any point
    `p \in U`, are called the *coordinates* of the chart `(U, \varphi)`.

    INPUT:

    - ``domain`` -- open subset `U` on which the chart is defined (must be
      an instance of :class:`~sage.manifolds.manifold.TopologicalManifold`)
    - ``coordinates`` -- (default: ``''`` (empty string)) the string
      defining the coordinate symbols, see below
    - ``names`` -- (default: ``None``) unused argument, except if
      ``coordinates`` is not provided; it must then be a tuple containing
      the coordinate symbols (this is guaranteed if the shortcut operator
      ``<,>`` is used)

    The string ``coordinates`` has the space ``' '`` as a separator and each
    item has at most two fields, separated by a colon (``:``):

    1. the coordinate symbol (a letter or a few letters);
    2. (optional) the LaTeX spelling of the coordinate, if not provided the
       coordinate symbol given in the first field will be used.

    If it contains any LaTeX expression, the string ``coordinates`` must be
    declared with the prefix 'r' (for "raw") to allow for a proper treatment
    of LaTeX's backslash character (see examples below).
    If no LaTeX spelling is to be set for any coordinate, the argument
    ``coordinates`` can be omitted when the shortcut operator ``<,>`` is
    used via Sage preparser (see examples below).

    EXAMPLES:

    A chart on a complex 2-dimensional topological manifold::

        sage: M = Manifold(2, 'M', field='complex', structure='topological')
        sage: X = M.chart('x y'); X
        Chart (M, (x, y))
        sage: latex(X)
        \left(M,(x, y)\right)
        sage: type(X)
        <class 'sage.manifolds.chart.Chart'>

    To manipulate the coordinates `(x,y)` as global variables,
    one has to set::

        sage: x,y = X[:]

    However, a shortcut is to use the declarator ``<x,y>`` in the left-hand
    side of the chart declaration (there is then no need to pass the string
    ``'x y'`` to ``chart()``)::

        sage: M = Manifold(2, 'M', field='complex', structure='topological')
        sage: X.<x,y> = M.chart(); X
        Chart (M, (x, y))

    The coordinates are then immediately accessible::

        sage: y
        y
        sage: x is X[0] and y is X[1]
        True

    Note that ``x`` and ``y`` declared in ``<x,y>`` are mere Python variable
    names and do not have to coincide with the coordinate symbols;
    for instance, one may write::

        sage: M = Manifold(2, 'M', field='complex', structure='topological')
        sage: X.<x1,y1> = M.chart('x y'); X
        Chart (M, (x, y))

    Then ``y`` is not known as a global Python variable and the
    coordinate `y` is accessible only through the global variable ``y1``::

        sage: y1
        y
        sage: latex(y1)
        y
        sage: y1 is X[1]
        True

    However, having the name of the Python variable coincide with the
    coordinate symbol is quite convenient; so it is recommended to declare::

        sage: M = Manifold(2, 'M', field='complex', structure='topological')
        sage: X.<x,y> = M.chart()

    In the above example, the chart X covers entirely the manifold ``M``::

        sage: X.domain()
        Complex 2-dimensional topological manifold M

    Of course, one may declare a chart only on an open subset of ``M``::

        sage: U = M.open_subset('U')
        sage: Y.<z1, z2> = U.chart(r'z1:\zeta_1 z2:\zeta_2'); Y
        Chart (U, (z1, z2))
        sage: Y.domain()
        Open subset U of the Complex 2-dimensional topological manifold M

    In the above declaration, we have also specified some LaTeX writing
    of the coordinates different from the text one::

        sage: latex(z1)
        {\zeta_1}

    Note the prefix ``r`` in front of the string ``r'z1:\zeta_1 z2:\zeta_2'``;
    it makes sure that the backslash character is treated as an ordinary
    character, to be passed to the LaTeX interpreter.

    Coordinates are Sage symbolic variables (see
    :mod:`sage.symbolic.expression`)::

        sage: type(z1)
        <type 'sage.symbolic.expression.Expression'>

    In addition to the Python variable name provided in the operator ``<.,.>``,
    the coordinates are accessible by their indices::

        sage: Y[0], Y[1]
        (z1, z2)

    The index range is that declared during the creation of the manifold. By
    default, it starts at 0, but this can be changed via the parameter
    ``start_index``::

        sage: M1 = Manifold(2, 'M_1', field='complex', structure='topological',
        ....:               start_index=1)
        sage: Z.<u,v> = M1.chart()
        sage: Z[1], Z[2]
        (u, v)

    The full set of coordinates is obtained by means of the slice
    operator ``[:]``::

        sage: Y[:]
        (z1, z2)

    Some partial sets of coordinates::

        sage: Y[:1]
        (z1,)
        sage: Y[1:]
        (z2,)

    Each constructed chart is automatically added to the manifold's user
    atlas::

        sage: M.atlas()
        [Chart (M, (x, y)), Chart (U, (z1, z2))]

    and to the atlas of the chart's domain::

        sage: U.atlas()
        [Chart (U, (z1, z2))]

    Manifold subsets have a *default chart*, which, unless changed via the
    method
    :meth:`~sage.manifolds.manifold.TopologicalManifold.set_default_chart`,
    is the first defined chart on the subset (or on a open subset of it)::

        sage: M.default_chart()
        Chart (M, (x, y))
        sage: U.default_chart()
        Chart (U, (z1, z2))

    The default charts are not privileged charts on the manifold, but rather
    charts whose name can be skipped in the argument list of functions having
    an optional ``chart=`` argument.

    The chart map `\varphi` acting on a point is obtained by passing
    it as an input to the map::

        sage: p = M.point((1+i, 2), chart=X); p
        Point on the Complex 2-dimensional topological manifold M
        sage: X(p)
        (I + 1, 2)
        sage: X(p) == p.coord(X)
        True

    .. SEEALSO::

        :class:`sage.manifolds.chart.RealChart` for charts on topological
        manifolds over `\RR`.

    """
    def __init__(self, domain, coordinates='', names=None):
        r"""
        Construct a chart.

        TESTS::

            sage: M = Manifold(2, 'M', field='complex', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: X
            Chart (M, (x, y))
            sage: type(X)
            <class 'sage.manifolds.chart.Chart'>
            sage: assumptions() # no assumptions on x,y set by X._init_coordinates
            []
            sage: TestSuite(X).run()

        """
        from sage.manifolds.manifold import TopologicalManifold
        if not isinstance(domain, TopologicalManifold):
            raise TypeError("the first argument must be an open subset of " +
                            "a topological manifold")
        if coordinates == '':
            for x in names:
                coordinates += x + ' '
            coordinates = coordinates[:-1]
        self._manifold = domain.manifold()
        self._domain = domain
        # Treatment of the coordinates:
        if ' ' in coordinates:
            coord_list = coordinates.split()
        else:
            coord_list = [coordinates]
        if len(coord_list) != self._manifold.dim():
            raise ValueError("the list of coordinates must contain " +
                             "{} elements".format(self._manifold.dim()))
        # The treatment of coordinates is performed by a seperate method,
        # _init_coordinates, which sets self._xx and
        # which may be redefined for subclasses (for instance RealChart).
        self._init_coordinates(coord_list)
        coord_string = ' '.join(str(x) for x in self._xx)
        if coord_string in self._domain._charts_by_coord:
            raise ValueError("the chart with coordinates " + coord_string +
                             " has already been declared on " +
                             "the {}".format(self._domain))
        self._domain._charts_by_coord[coord_string] = self
        #
        # Additional restrictions on the coordinates
        self._restrictions = []  # to be set with method add_restrictions()
        #
        # The chart is added to the domain's atlas, as well as to all the
        # atlases of the domain's supersets; moreover the fist defined chart
        # is considered as the default chart
        for sd in self._domain._supersets:
            # the chart is added in the top charts only if its coordinates have
            # not been used:
            for chart in sd._atlas:
                if self._xx == chart._xx:
                    break
            else:
                sd._top_charts.append(self)
            sd._atlas.append(self)
            if sd._def_chart is None:
                sd._def_chart = self
        # The chart is added to the list of the domain's covering charts:
        self._domain._covering_charts.append(self)
        # Initialization of the set of charts that are restrictions of the
        # current chart to subsets of the chart domain:
        self._subcharts = set([self])
        # Initialization of the set of charts which the current chart is a
        # restriction of:
        self._supercharts = set([self])
        #
        self._dom_restrict = {} # dict. of the restrictions of self to
                                # subsets of self._domain, with the
                                # subsets as keys

    def _init_coordinates(self, coord_list):
        r"""
        Initialization of the coordinates as symbolic variables.

        This method must be redefined by derived classes in order to take
        into account specificities (e.g. enforcing real coordinates).

        INPUT:

        - ``coord_list`` -- list of coordinate fields, which items in each
          field separated by ":"; there are at most 2 items per field:
          the coordinate name and the coordinate LaTeX symbol

        TESTS::

            sage: M = Manifold(2, 'M', field='complex', structure='topological')
            sage: X.<z1, z2> = M.chart()
            sage: X._init_coordinates(['z1', 'z2'])
            sage: X
            Chart (M, (z1, z2))
            sage: X._init_coordinates([r'z1:\zeta_1', r'z2:\zeta_2'])
            sage: X
            Chart (M, (z1, z2))
            sage: latex(X)
            \left(M,({\zeta_1}, {\zeta_2})\right)

        """
        xx_list = [] # will contain the coordinates as Sage symbolic variables
        for coord_field in coord_list:
            coord_properties = coord_field.split(':')
            coord_symb = coord_properties[0].strip() # the coordinate symbol
            # LaTeX symbol:
            coord_latex = None
            for prop in coord_properties[1:]:
                coord_latex = prop.strip()
            # Construction of the coordinate as some Sage's symbolic variable:
            coord_var = SR.var(coord_symb, latex_name=coord_latex)
            xx_list.append(coord_var)
        self._xx = tuple(xx_list)

    def _repr_(self):
        r"""
        String representation of the object.

        TESTS::

            sage: M = Manifold(2, 'M', field='complex', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: X
            Chart (M, (x, y))

        """
        return 'Chart ({}, {})'.format(self._domain._name, self._xx)

    def _latex_(self):
        r"""
        LaTeX representation of the object.

        TESTS::

            sage: M = Manifold(2, 'M', field='complex', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: X._latex_()
            '\\left(M,(x, y)\\right)'
            sage: Y.<z1, z2> = M.chart(r'z1:\zeta_1 z2:\zeta2')
            sage: Y._latex_()
            '\\left(M,({\\zeta_1}, {\\zeta2})\\right)'
            sage: latex(Y)
            \left(M,({\zeta_1}, {\zeta2})\right)

        """
        description = r'\left(' + latex(self._domain).strip() + ',('
        n = len(self._xx)
        for i in range(n-1):
            description += latex(self._xx[i]).strip() + ', '
        description += latex(self._xx[n-1]).strip() + r')\right)'
        return description

    def _first_ngens(self, n):
        r"""
        Return the list of coordinates.

        This is useful only for the use of Sage preparser::

            sage: preparse("c_cart.<x,y,z> = M.chart()")
            "c_cart = M.chart(names=('x', 'y', 'z',)); (x, y, z,) = c_cart._first_ngens(3)"

        """
        return self[:]

    def __getitem__(self, i):
        r"""
        Access to the coordinates.

        INPUT:

        - ``i`` -- index of the coordinate; if the slice ``[:]``, then all
            the coordinates are returned

        OUTPUT:

        - the coordinate of index ``i`` or all the coordinates (as a tuple)
          if ``i`` is the slice ``[:]``

        EXAMPLES::

            sage: M = Manifold(2, 'M', field='complex', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: X[0]
            x
            sage: X[1]
            y
            sage: X[:]
            (x, y)

        The index range is controlled by the parameter ``start_index``::

            sage: M = Manifold(2, 'M', field='complex', structure='topological',
            ....:              start_index=1)
            sage: X.<x,y> = M.chart()
            sage: X[1]
            x
            sage: X[2]
            y
            sage: X[:]
            (x, y)

        We check that slices are properly shifted as well::

            sage: X[2:]
            (y,)
            sage: X[:2]
            (x,)
        """
        if isinstance(i, slice):
            start,stop = i.start,i.stop
            if start is not None:
                start -= self._manifold._sindex
            if stop is not None:
                stop -= self._manifold._sindex
            return self._xx[start:stop:i.step]
        else:
            return self._xx[i-self._manifold._sindex]

    def __call__(self, point):
        r"""
        Return the coordinates of a given point.

        INPUT:

        - ``point`` -- point in the domain of the chart

        OUTPUT:

        - tuple of the coordinates of the point

        EXAMPLES::

            sage: M = Manifold(2, 'M', field='complex', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: p = M.point((1+i, 2-i), chart=X)
            sage: X(p)
            (I + 1, -I + 2)
            sage: X(M.an_element())
            (0, 0)

        """
        return point.coord(self)

    def domain(self):
        r"""
        Return the open subset on which the chart is defined.

        EXAMPLES::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: X.domain()
            2-dimensional topological manifold M
            sage: U = M.open_subset('U')
            sage: Y.<u,v> = U.chart()
            sage: Y.domain()
            Open subset U of the 2-dimensional topological manifold M

        """
        return self._domain

    def manifold(self):
        r"""
        Return the manifold on which the chart is defined.

        EXAMPLES::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: U = M.open_subset('U')
            sage: X.<x,y> = U.chart()
            sage: X.manifold()
            2-dimensional topological manifold M
            sage: X.domain()
            Open subset U of the 2-dimensional topological manifold M

        """
        return self._manifold

    def add_restrictions(self, restrictions):
        r"""
        Add some restrictions on the coordinates.

        INPUT:

        - ``restrictions`` -- list of restrictions on the
          coordinates, in addition to the ranges declared by the intervals
          specified in the chart constructor

        A restriction can be any symbolic equality or inequality involving
        the coordinates, such as ``x > y`` or ``x^2 + y^2 != 0``. The items
        of the list ``restrictions`` are combined with the ``and`` operator;
        if some restrictions are to be combined with the ``or`` operator
        instead, they have to be passed as a tuple in some single item
        of the list ``restrictions``. For example::

          restrictions = [x > y, (x != 0, y != 0), z^2 < x]

        means (``x > y``) and ((``x != 0``) or (``y != 0``)) and
        (``z^2 < x``). If the list ``restrictions`` contains only one
        item, this item can be passed as such, i.e. writing ``x > y``
        instead of the single element list ``[x > y]``.

        EXAMPLES::

            sage: M = Manifold(2, 'M', field='complex', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: X.add_restrictions(abs(x) > 1)
            sage: X.valid_coordinates(2+i, 1)
            True
            sage: X.valid_coordinates(i, 1)
            False

        """
        if not isinstance(restrictions, list):
            # case of a single condition or conditions to be combined by "or"
            restrictions = [restrictions]
        self._restrictions.extend(restrictions)

    def restrict(self, subset, restrictions=None):
        r"""
        Return the restriction of the chart to some open subset of its domain.

        If the current chart is `(U,\varphi)`, a *restriction* (or *subchart*)
        is a chart `(V,\psi)` such that `V\subset U` and `\psi = \varphi |_V`.

        If such subchart has not been defined yet, it is constructed here.

        The coordinates of the subchart bare the same names as the coordinates
        of the current chart.

        INPUT:

        - ``subset`` -- open subset `V` of the chart domain `U` (must be an
          instance of :class:`~sage.manifolds.manifold.TopologicalManifold`)
        - ``restrictions`` -- (default: ``None``) list of coordinate
          restrictions defining the subset `V`

        A restriction can be any symbolic equality or inequality involving
        the coordinates, such as ``x > y`` or ``x^2 + y^2 != 0``. The items
        of the list ``restrictions`` are combined with the ``and`` operator;
        if some restrictions are to be combined with the ``or`` operator
        instead, they have to be passed as a tuple in some single item
        of the list ``restrictions``. For example::

          restrictions = [x > y, (x != 0, y != 0), z^2 < x]

        means (``x > y``) and ((``x != 0``) or (``y != 0``)) and
        (``z^2 < x``). If the list ``restrictions`` contains only one
        item, this item can be passed as such, i.e. writing ``x > y``
        instead of the single element list ``[x > y]``.

        OUTPUT:

        - chart `(V,\psi)`, as an instance of :class:`Chart`.

        EXAMPLES:

        Coordinates on the unit open ball of  `\CC^2` as a subchart
        of the global coordinates of `\CC^2`::

            sage: M = Manifold(2, 'C^2', field='complex', structure='topological')
            sage: X.<z1, z2> = M.chart()
            sage: B = M.open_subset('B')
            sage: X_B = X.restrict(B, abs(z1)^2 + abs(z2)^2 < 1); X_B
            Chart (B, (z1, z2))

        """
        if subset == self._domain:
            return self
        if subset not in self._dom_restrict:
            if not subset.is_subset(self._domain):
                raise ValueError("the specified subset is not a subset " +
                                 "of the domain of definition of the chart")
            coordinates = ""
            for coord in self._xx:
                coordinates += repr(coord) + ' '
            res = type(self)(subset, coordinates)
            res._restrictions.extend(self._restrictions)
            # The coordinate restrictions are added to the result chart and
            # possibly transformed into coordinate bounds:
            if restrictions is not None:
                res.add_restrictions(restrictions)
            # Update of supercharts and subcharts:
            res._supercharts.update(self._supercharts)
            for schart in self._supercharts:
                schart._subcharts.add(res)
                schart._dom_restrict[subset] = res
            # Update of domain restrictions:
            self._dom_restrict[subset] = res
        return self._dom_restrict[subset]

    def valid_coordinates(self, *coordinates, **kwds):
        r"""
        Check whether a tuple of coordinates can be the coordinates of a
        point in the chart domain.

        INPUT:

        - ``*coordinates`` -- coordinate values
        - ``**kwds`` -- options:

          - ``parameters=None``, dictionary to set numerical values to
            some parameters (see example below)

        OUTPUT:

        - ``True`` if the coordinate values are admissible in the chart
          image, ``False`` otherwise

        EXAMPLES::

            sage: M = Manifold(2, 'M', field='complex', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: X.add_restrictions([abs(x)<1, y!=0])
            sage: X.valid_coordinates(0, i)
            True
            sage: X.valid_coordinates(i, 1)
            False
            sage: X.valid_coordinates(i/2, 1)
            True
            sage: X.valid_coordinates(i/2, 0)
            False
            sage: X.valid_coordinates(2, 0)
            False

        Example of use with the keyword ``parameters`` to set a specific value
        to a parameter appearing in the coordinate restrictions::

            sage: var('a')  # the parameter is a symbolic variable
            a
            sage: Y.<u,v> = M.chart()
            sage: Y.add_restrictions(abs(v)<a)
            sage: Y.valid_coordinates(1, i, parameters={a: 2})  # setting a=2
            True
            sage: Y.valid_coordinates(1, 2*i, parameters={a: 2})
            False

        """
        if len(coordinates) != self._domain._dim:
            return False
        if 'parameters' in kwds:
            parameters = kwds['parameters']
        else:
            parameters = None
        # Check of restrictions:
        if self._restrictions:
            substitutions = dict(zip(self._xx, coordinates))
            if parameters:
                substitutions.update(parameters)
            for restrict in self._restrictions:
                if isinstance(restrict, tuple): # case of or conditions
                    combine = False
                    for expr in restrict:
                        combine = combine or bool(expr.subs(substitutions))
                    if not combine:
                        return False
                else:
                    if not bool(restrict.subs(substitutions)):
                        return False
        # All tests have been passed:
        return True

    def transition_map(self, other, transformations, intersection_name=None,
                       restrictions1=None, restrictions2=None):
        r"""
        Construct the transition map between the current chart,
        `(U, \varphi)` say, and another one, `(V, \psi)` say.

        If `n` is the manifold's dimension, the *transition map*
        is the map

        .. MATH::

            \psi\circ\varphi^{-1}: \varphi(U\cap V) \subset K^n
            \rightarrow \psi(U\cap V) \subset K^n,

        where `K` is the manifold's base field. In other words, the
        transition map expresses the coordinates `(y^1, \ldots, y^n)` of
        `(V, \psi)` in terms of the coordinates `(x^1, \ldots, x^n)` of
        `(U, \varphi)` on the open subset where the two charts intersect,
        i.e. on `U \cap V`.

        INPUT:

        - ``other`` -- the chart `(V, \psi)`
        - ``transformations`` -- tuple (or list) `(Y_1, \ldots, Y_n)`, where
          `Y_i` is the symbolic expression of the coordinate `y^i` in terms
          of the coordinates `(x^1, \ldots, x^n)`
        - ``intersection_name`` -- (default: ``None``) name to be given to the
          subset `U \cap V` if the latter differs from `U` or `V`
        - ``restrictions1`` -- (default: ``None``) list of conditions on the
          coordinates of the current chart that define `U \cap V` if the
          latter differs from `U`
        - ``restrictions2`` -- (default: ``None``) list of conditions on the
          coordinates of the chart `(V,\psi)` that define `U \cap V` if the
          latter differs from `V`

        A restriction can be any symbolic equality or inequality involving
        the coordinates, such as ``x > y`` or ``x^2 + y^2 != 0``. The items
        of the list ``restrictions`` are combined with the ``and`` operator;
        if some restrictions are to be combined with the ``or`` operator
        instead, they have to be passed as a tuple in some single item
        of the list ``restrictions``. For example::

          restrictions = [x > y, (x != 0, y != 0), z^2 < x]

        means (``x > y``) and ((``x != 0``) or (``y != 0``)) and
        (``z^2 < x``). If the list ``restrictions`` contains only one
        item, this item can be passed as such, i.e. writing ``x > y``
        instead of the single element list ``[x > y]``.

        OUTPUT:

        - the transition map `\psi \circ \varphi^{-1}` defined on
          `U \cap V`, as an instance of :class:`CoordChange`

        EXAMPLES:

        Transition map between two stereographic charts on the circle `S^1`::

            sage: M = Manifold(1, 'S^1', structure='topological')
            sage: U = M.open_subset('U') # Complement of the North pole
            sage: cU.<x> = U.chart() # Stereographic chart from the North pole
            sage: V = M.open_subset('V') # Complement of the South pole
            sage: cV.<y> = V.chart() # Stereographic chart from the South pole
            sage: M.declare_union(U,V)   # S^1 is the union of U and V
            sage: trans = cU.transition_map(cV, 1/x, intersection_name='W',
            ....:                           restrictions1= x!=0, restrictions2 = y!=0)
            sage: trans
            Change of coordinates from Chart (W, (x,)) to Chart (W, (y,))
            sage: trans.display()
            y = 1/x

        The subset `W`, intersection of `U` and `V`, has been created by
        ``transition_map()``::

            sage: M.list_of_subsets()
            [1-dimensional topological manifold S^1,
             Open subset U of the 1-dimensional topological manifold S^1,
             Open subset V of the 1-dimensional topological manifold S^1,
             Open subset W of the 1-dimensional topological manifold S^1]
            sage: W = M.list_of_subsets()[3]
            sage: W is U.intersection(V)
            True
            sage: M.atlas()
            [Chart (U, (x,)), Chart (V, (y,)), Chart (W, (x,)), Chart (W, (y,))]

        Transition map between the spherical chart and the Cartesian
        one on `\RR^2`::

            sage: M = Manifold(2, 'R^2', structure='topological')
            sage: c_cart.<x,y> = M.chart()
            sage: U = M.open_subset('U') # the complement of the half line {y=0, x >= 0}
            sage: c_spher.<r,phi> = U.chart(r'r:(0,+oo) phi:(0,2*pi):\phi')
            sage: trans = c_spher.transition_map(c_cart, (r*cos(phi), r*sin(phi)),
            ....:                                restrictions2=(y!=0, x<0))
            sage: trans
            Change of coordinates from Chart (U, (r, phi)) to Chart (U, (x, y))
            sage: trans.display()
            x = r*cos(phi)
            y = r*sin(phi)

        In this case, no new subset has been created since `U \cap M = U`::

            sage: M.list_of_subsets()
            [2-dimensional topological manifold R^2,
             Open subset U of the 2-dimensional topological manifold R^2]

        but a new chart has been created: `(U, (x, y))`::

            sage: M.atlas()
            [Chart (R^2, (x, y)), Chart (U, (r, phi)), Chart (U, (x, y))]

        """
        dom1 = self._domain
        dom2 = other._domain
        dom = dom1.intersection(dom2, name=intersection_name)
        if dom is dom1:
            chart1 = self
        else:
            chart1 = self.restrict(dom, restrictions1)
        if dom is dom2:
            chart2 = other
        else:
            chart2 = other.restrict(dom, restrictions2)
        if not isinstance(transformations, (tuple, list)):
                transformations = [transformations]
        return CoordChange(chart1, chart2, *transformations)

#*****************************************************************************

class RealChart(Chart):
    r"""
    Chart on a topological manifold over `\RR`.

    Given a topological manifold `M` of dimension `n` over `\RR`, a *chart*
    on `M` is a pair `(U,\varphi)`, where `U` is an open subset of `M` and
    `\varphi : U \to V \subset \RR^n` is a homeomorphism from `U` to
    an open subset `V` of `\RR^n`.

    The components `(x^1, \ldots, x^n)` of `\varphi`, defined by
    `\varphi(p) = (x^1(p), \ldots, x^n(p))\in \RR^n` for any point
    `p \in U`, are called the *coordinates* of the chart `(U, \varphi)`.

    INPUT:

    - ``domain`` -- open subset `U` on which the chart is defined
    - ``coordinates`` -- (default: ``''`` (empty string)) string defining
      the coordinate symbols and ranges, see below
    - ``names`` -- (default: ``None``) unused argument, except if
      ``coordinates`` is not provided; it must then be a tuple containing
      the coordinate symbols (this is guaranteed if the shortcut operator
      ``<,>`` is used)

    The string ``coordinates`` has the space ``' '`` as a separator and each
    item has at most three fields, separated by a colon (``:``):

    1. The coordinate symbol (a letter or a few letters).
    2. (optional) The interval `I` defining the coordinate range: if not
       provided, the coordinate is assumed to span all `\RR`; otherwise
       `I` must be provided in the form ``(a,b)`` (or equivalently
       ``]a,b[``). The bounds ``a`` and ``b`` can be ``+/-Infinity``,
       ``Inf``, ``infinity``, ``inf`` or ``oo``.
       For *singular* coordinates, non-open intervals such as ``[a,b]`` and
       ``(a,b]`` (or equivalently ``]a,b]``) are allowed.
       Note that the interval declaration must not contain any whitespace.
    3. (optional) The LaTeX spelling of the coordinate; if not provided the
       coordinate symbol given in the first field will be used.

    The order of the fields 2 and 3 does not matter and each of them can be
    omitted. If it contains any LaTeX expression, the string ``coordinates``
    must be declared with the prefix 'r' (for "raw") to allow for a proper
    treatment of LaTeX backslash characters (see examples below). If no
    interval range and no LaTeX spelling is to be set for any coordinate,
    the argument ``coordinates`` can be omitted when the shortcut
    operator ``<,>`` is used via Sage preparser (see examples below).

    EXAMPLES:

    Cartesian coordinates on `\RR^3`::

        sage: M = Manifold(3, 'R^3', r'\RR^3', structure='topological',
        ....:              start_index=1)
        sage: c_cart = M.chart('x y z'); c_cart
        Chart (R^3, (x, y, z))
        sage: type(c_cart)
        <class 'sage.manifolds.chart.RealChart'>

    To have the coordinates accessible as global variables, one has to set::

        sage: (x,y,z) = c_cart[:]

    However, a shortcut is to use the declarator ``<x,y,z>`` in the left-hand
    side of the chart declaration (there is then no need to pass the string
    ``'x y z'`` to  ``chart()``)::

        sage: M = Manifold(3, 'R^3', r'\RR^3', structure='topological',
        ....:              start_index=1)
        sage: c_cart.<x,y,z> = M.chart(); c_cart
        Chart (R^3, (x, y, z))

    The coordinates are then immediately accessible::

        sage: y
        y
        sage: y is c_cart[2]
        True

    Note that ``x, y, z`` declared in ``<x,y,z>`` are mere Python variable
    names and do not have to coincide with the coordinate symbols; for
    instance, one may write::

        sage: M = Manifold(3, 'R^3', r'\RR^3', structure='topological', start_index=1)
        sage: c_cart.<x1,y1,z1> = M.chart('x y z'); c_cart
        Chart (R^3, (x, y, z))

    Then ``y`` is not known as a global variable and the coordinate `y`
    is accessible only through the global variable ``y1``::

        sage: y1
        y
        sage: y1 is c_cart[2]
        True

    However, having the name of the Python variable coincide with the
    coordinate symbol is quite convenient; so it is recommended to declare::

        sage: forget()   # for doctests only
        sage: M = Manifold(3, 'R^3', r'\RR^3', structure='topological', start_index=1)
        sage: c_cart.<x,y,z> = M.chart()

    Spherical coordinates on the subset `U` of `\RR^3` that is the
    complement of the half-plane `\{y=0, x \geq 0\}`::

        sage: U = M.open_subset('U')
        sage: c_spher.<r,th,ph> = U.chart(r'r:(0,+oo) th:(0,pi):\theta ph:(0,2*pi):\phi')
        sage: c_spher
        Chart (U, (r, th, ph))

    Note the prefix 'r' for the string defining the coordinates in the
    arguments of ``chart``.

    Coordinates are Sage symbolic variables (see
    :mod:`sage.symbolic.expression`)::

        sage: type(th)
        <type 'sage.symbolic.expression.Expression'>
        sage: latex(th)
        {\theta}
        sage: assumptions(th)
        [th is real, th > 0, th < pi]

    Coordinate are also accessible by their indices::

        sage: x1 = c_spher[1]; x2 = c_spher[2]; x3 = c_spher[3]
        sage: print x1, x2, x3
        r th ph
        sage: (x1, x2, x3) == (r, th, ph)
        True

    The full set of coordinates is obtained by means of the slice ``[:]``::

        sage: c_cart[:]
        (x, y, z)
        sage: c_spher[:]
        (r, th, ph)

    Let us check that the declared coordinate ranges have been taken into
    account::

        sage: c_cart.coord_range()
        x: (-oo, +oo); y: (-oo, +oo); z: (-oo, +oo)
        sage: c_spher.coord_range()
        r: (0, +oo); th: (0, pi); ph: (0, 2*pi)
        sage: bool(th>0 and th<pi)
        True
        sage: assumptions()  # list all current symbolic assumptions
        [x is real, y is real, z is real, r is real, r > 0, th is real,
         th > 0, th < pi, ph is real, ph > 0, ph < 2*pi]

    The coordinate ranges are used for simplifications::

        sage: simplify(abs(r)) # r has been declared to lie in the interval (0,+oo)
        r
        sage: simplify(abs(x)) # no positive range has been declared for x
        abs(x)

    Each constructed chart is automatically added to the manifold's
    user atlas::

        sage: M.atlas()
        [Chart (R^3, (x, y, z)), Chart (U, (r, th, ph))]

    and to the atlas of its domain::

        sage: U.atlas()
        [Chart (U, (r, th, ph))]

    Manifold subsets have a *default chart*, which, unless changed
    via the method
    :meth:`~sage.manifolds.manifold.TopologicalManifold.set_default_chart`,
    is the first defined chart on the subset (or on a open subset of it)::

        sage: M.default_chart()
        Chart (R^3, (x, y, z))
        sage: U.default_chart()
        Chart (U, (r, th, ph))

    The default charts are not privileged charts on the manifold, but rather
    charts whose name can be skipped in the argument list of functions having
    an optional ``chart=`` argument.

    The chart map `\varphi` acting on a point is obtained by means of the
    call operator, i.e. the operator ``()``::

        sage: p = M.point((1,0,-2)); p
        Point on the 3-dimensional topological manifold R^3
        sage: c_cart(p)
        (1, 0, -2)
        sage: c_cart(p) == p.coord(c_cart)
        True
        sage: q = M.point((2,pi/2,pi/3), chart=c_spher) # point defined by its spherical coordinates
        sage: c_spher(q)
        (2, 1/2*pi, 1/3*pi)
        sage: c_spher(q) == q.coord(c_spher)
        True
        sage: a = U.point((1,pi/2,pi)) # the default coordinates on U are the spherical ones
        sage: c_spher(a)
        (1, 1/2*pi, pi)
        sage: c_spher(a) == a.coord(c_spher)
        True

    Cartesian coordinates on `U` as an example of chart construction with
    coordinate restrictions: since `U` is the complement of the half-plane
    `\{y = 0, x \geq 0\}`, we must have `y \neq 0` or `x < 0` on U.
    Accordingly, we set::

        sage: c_cartU.<x,y,z> = U.chart()
        sage: c_cartU.add_restrictions((y!=0, x<0))
        sage: U.atlas()
        [Chart (U, (r, th, ph)), Chart (U, (x, y, z))]
        sage: M.atlas()
        [Chart (R^3, (x, y, z)), Chart (U, (r, th, ph)), Chart (U, (x, y, z))]
        sage: c_cartU.valid_coordinates(-1,0,2)
        True
        sage: c_cartU.valid_coordinates(1,0,2)
        False
        sage: c_cart.valid_coordinates(1,0,2)
        True

    Note that, as an example, the following would have meant `y \neq 0`
    *and* `x < 0`::

        c_cartU.add_restrictions([y!=0, x<0])
    """
    def __init__(self, domain, coordinates='', names=None):
        r"""
        Construct a chart on a real topological manifold.

        TESTS::

            sage: forget()  # for doctests only
            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: X
            Chart (M, (x, y))
            sage: type(X)
            <class 'sage.manifolds.chart.RealChart'>
            sage: assumptions()  # assumptions set in X._init_coordinates
            [x is real, y is real]
            sage: TestSuite(X).run()

        """
        Chart.__init__(self, domain, coordinates=coordinates, names=names)

    def _init_coordinates(self, coord_list):
        r"""
        Initialization of the coordinates as symbolic variables.

        This method must be redefined by derived classes in order to take
        into account specificities (e.g. enforcing real coordinates).

        INPUT:

        - ``coord_list`` -- list of coordinate fields, which items in each
          field separated by ":"; there are at most 3 items per field:
          the coordinate name, the coordinate LaTeX symbol and the
          coordinate range

        TESTS::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: X._init_coordinates(['x', 'y'])
            sage: X
            Chart (M, (x, y))
            sage: latex(X)
            \left(M,(x, y)\right)
            sage: X.coord_range()
            x: (-oo, +oo); y: (-oo, +oo)
            sage: X._init_coordinates([r'x1:\xi:(0,1)', r'y1:\eta'])
            sage: X
            Chart (M, (x1, y1))
            sage: latex(X)
            \left(M,({\xi}, {\eta})\right)
            sage: X.coord_range()
            x1: (0, 1); y1: (-oo, +oo)

        """
        from sage.symbolic.assumptions import assume
        xx_list = [] # will contain the coordinates as Sage symbolic variables
        bounds_list = [] # will contain the coordinate bounds
        for coord_field in coord_list:
            coord_properties = coord_field.split(':')
            coord_symb = coord_properties[0].strip() # the coordinate symbol
            # default values, possibly redefined below:
            coord_latex = None
            xmin = -Infinity; xmin_included = False
            xmax = +Infinity; xmax_included = False
            # scan of the properties other than the symbol:
            for prop in coord_properties[1:]:
                prop1 = prop.strip()
                delim_min = prop1[0]
                if delim_min in ['[', ']', '(']:
                    # prop1 is the coordinate's range
                    xmin_str, xmax_str = prop1[1:len(prop1)-1].split(',')
                    if xmin_str not in ['-inf', '-Inf', '-infinity',
                                        '-Infinity', '-oo']:
                        xmin = SR(xmin_str)
                        xmin_included = ( delim_min == '[' )
                    if xmax_str not in ['inf', '+inf', 'Inf', '+Inf',
                                        'infinity', '+infinity', 'Infinity',
                                        '+Infinity', 'oo', '+oo']:
                        xmax = SR(xmax_str)
                        xmax_included = ( prop1[-1] == ']' )
                else:
                    # prop1 is the coordinate's LaTeX symbol
                    coord_latex = prop1
            # Construction of the coordinate as some Sage's symbolic variable:
            coord_var = SR.var(coord_symb, domain='real',
                               latex_name=coord_latex)
            assume(coord_var, 'real')
            if xmin != -Infinity:
                if xmin_included:
                    assume(coord_var >= xmin)
                else:
                    assume(coord_var > xmin)
            if xmax != Infinity:
                if xmax_included:
                    assume(coord_var <= xmax)
                else:
                    assume(coord_var < xmax)
            xx_list.append(coord_var)
            bounds_list.append(((xmin, xmin_included), (xmax, xmax_included)))
        self._xx = tuple(xx_list)
        self._bounds = tuple(bounds_list)

    def coord_bounds(self, i=None):
        r"""
        Return the lower and upper bounds of the range of a coordinate.

        For a nicely formatted output, use :meth:`coord_range` instead.

        INPUT:

        - ``i`` -- (default: ``None``)  index of the coordinate; if ``None``,
          the bounds of all the coordinates are returned

        OUTPUT:

        - the coordinate bounds as the tuple
          ``((xmin, min_included), (xmax, max_included))`` where

          - ``xmin`` is the coordinate lower bound
          - ``min_included`` is a boolean, indicating whether the coordinate
            can take the value ``xmin``, i.e. ``xmin`` is a strict lower
            bound iff ``min_included`` is ``False``
          - ``xmin`` is the coordinate upper bound
          - ``max_included`` is a boolean, indicating whether the coordinate
            can take the value ``xmax``, i.e. ``xmax`` is a strict upper
            bound iff ``max_included`` is ``False``

        EXAMPLES:

        Some coordinate bounds on a 2-dimensional manifold::

            sage: forget()  # for doctests only
            sage: M = Manifold(2, 'M', structure='topological')
            sage: c_xy.<x,y> = M.chart('x y:[0,1)')
            sage: c_xy.coord_bounds(0)  # x in (-oo,+oo) (the default)
            ((-Infinity, False), (+Infinity, False))
            sage: c_xy.coord_bounds(1)  # y in [0,1)
            ((0, True), (1, False))
            sage: c_xy.coord_bounds()
            (((-Infinity, False), (+Infinity, False)), ((0, True), (1, False)))
            sage: c_xy.coord_bounds() == (c_xy.coord_bounds(0), c_xy.coord_bounds(1))
            True

        The coordinate bounds can also be recovered via the method
        :meth:`coord_range`::

            sage: c_xy.coord_range()
            x: (-oo, +oo); y: [0, 1)
            sage: c_xy.coord_range(y)
            y: [0, 1)

        or via Sage's function
        :func:`sage.symbolic.assumptions.assumptions`::

            sage: assumptions(x)
            [x is real]
            sage: assumptions(y)
            [y is real, y >= 0, y < 1]

        """
        if i is None:
            return self._bounds
        else:
            return self._bounds[i-self._manifold._sindex]

    def coord_range(self, xx=None):
        r"""
        Display the range of a coordinate (or all coordinates), as an
        interval.

        INPUT:

        - ``xx`` -- (default: ``None``) symbolic expression corresponding
          to a coordinate of the current chart; if ``None``, the ranges of
          all coordinates are displayed

        EXAMPLES:

        Ranges of coordinates on a 2-dimensional manifold::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: X.coord_range()
            x: (-oo, +oo); y: (-oo, +oo)
            sage: X.coord_range(x)
            x: (-oo, +oo)
            sage: U = M.open_subset('U', coord_def={X: [x>1, y<pi]})
            sage: XU = X.restrict(U)  # restriction of chart X to U
            sage: XU.coord_range()
            x: (1, +oo); y: (-oo, pi)
            sage: XU.coord_range(x)
            x: (1, +oo)
            sage: XU.coord_range(y)
            y: (-oo, pi)

        The output is LaTeX-formatted for the notebook::

            sage: latex(XU.coord_range(y))
            y :\ \left( -\infty, \pi \right)

        """
        from sage.tensor.modules.format_utilities import FormattedExpansion
        def _display_coord_range(self, xx, rtxt, rlatex):
            ind = self._xx.index(xx)
            bounds = self._bounds[ind]
            rtxt += "{}: ".format(xx)
            rlatex += latex(xx) + r":\ "
            if bounds[0][1]:
                rtxt += "["
                rlatex += r"\left["
            else:
                rtxt += "("
                rlatex += r"\left("
            xmin = bounds[0][0]
            if xmin == -Infinity:
                rtxt += "-oo, "
                rlatex += r"-\infty,"
            else:
                rtxt += "{}, ".format(xmin)
                rlatex += latex(xmin) + ","
            xmax = bounds[1][0]
            if xmax == Infinity:
                rtxt += "+oo"
                rlatex += r"+\infty"
            else:
                rtxt += "{}".format(xmax)
                rlatex += latex(xmax)
            if bounds[1][1]:
                rtxt += "]"
                rlatex += r"\right]"
            else:
                rtxt += ")"
                rlatex += r"\right)"
            return rtxt, rlatex
        resu_txt = ""
        resu_latex = ""
        if xx is None:
            for x in self._xx:
                if resu_txt != "":
                    resu_txt += "; "
                    resu_latex += r";\quad "
                resu_txt, resu_latex = _display_coord_range(self, x, resu_txt,
                                                            resu_latex)
        else:
            resu_txt, resu_latex = _display_coord_range(self, xx, resu_txt,
                                                        resu_latex)
        return FormattedExpansion(resu_txt, resu_latex)


    def add_restrictions(self, restrictions):
        r"""
        Add some restrictions on the coordinates.

        INPUT:

        - ``restrictions`` -- list of restrictions on the
          coordinates, in addition to the ranges declared by the intervals
          specified in the chart constructor

        A restriction can be any symbolic equality or inequality involving
        the coordinates, such as ``x > y`` or ``x^2 + y^2 != 0``. The items
        of the list ``restrictions`` are combined with the ``and`` operator;
        if some restrictions are to be combined with the ``or`` operator
        instead, they have to be passed as a tuple in some single item
        of the list ``restrictions``. For example::

          restrictions = [x > y, (x != 0, y != 0), z^2 < x]

        means (``x > y``) and ((``x != 0``) or (``y != 0``)) and
        (``z^2 < x``). If the list ``restrictions`` contains only one
        item, this item can be passed as such, i.e. writing ``x > y``
        instead of the single element list ``[x > y]``.

        EXAMPLES:

        Cartesian coordinates on the open unit disc in `\RR^2`::

            sage: M = Manifold(2, 'M', structure='topological') # the open unit disc
            sage: X.<x,y> = M.chart()
            sage: X.add_restrictions(x^2+y^2<1)
            sage: X.valid_coordinates(0,2)
            False
            sage: X.valid_coordinates(0,1/3)
            True

        The restrictions are transmitted to subcharts::

            sage: A = M.open_subset('A') # annulus 1/2 < r < 1
            sage: X_A = X.restrict(A, x^2+y^2 > 1/4)
            sage: X_A._restrictions
            [x^2 + y^2 < 1, x^2 + y^2 > (1/4)]
            sage: X_A.valid_coordinates(0,1/3)
            False
            sage: X_A.valid_coordinates(2/3,1/3)
            True

        If appropriate, the restrictions are transformed into bounds on
        the coordinate ranges::

            sage: U = M.open_subset('U')
            sage: X_U = X.restrict(U)
            sage: X_U.coord_range()
            x: (-oo, +oo); y: (-oo, +oo)
            sage: X_U.add_restrictions([x<0, y>1/2])
            sage: X_U.coord_range()
            x: (-oo, 0); y: (1/2, +oo)

        """
        import operator
        if not isinstance(restrictions, list):
            # case of a single condition or conditions to be combined by "or"
            restrictions = [restrictions]
        self._restrictions.extend(restrictions)
        # Update of the coordinate bounds from the restrictions:
        bounds = list(self._bounds) # convert to a list for modifications
        new_restrictions = []
        for restrict in self._restrictions:
            restrict_used = False # determines whether restrict is used
                                  # to set some coordinate bound
            if not isinstance(restrict, tuple): # case of 'or' conditions
                                                # excluded
                operands = restrict.operands()
                left = operands[0]
                right = operands[1]
                right_var = right.variables()
                if left in self._xx:
                    # the l.h.s. of the restriction is a single
                    # coordinate
                    right_coord = [coord for coord in self._xx
                                   if coord in right_var]
                    if not right_coord:
                        # there is no other coordinate in the r.h.s.
                        ind = self._xx.index(left)
                        left_bounds = list(bounds[ind])
                        oper = restrict.operator()
                        oinf = left_bounds[0][0] # old coord inf
                        osup = left_bounds[1][0] # old coord sup
                        if oper == operator.lt:
                            if osup == Infinity or right <= osup:
                                left_bounds[1] = (right, False)
                                restrict_used = True
                        elif oper == operator.le:
                            if osup == Infinity or right < osup:
                                left_bounds[1] = (right, True)
                                restrict_used = True
                        elif oper == operator.gt:
                            if oinf == -Infinity or right >= oinf:
                                left_bounds[0] = (right, False)
                                restrict_used = True
                        elif oper == operator.ge:
                            if oinf == -Infinity or right > oinf:
                                left_bounds[0] = (right, True)
                                restrict_used = True
                        bounds[ind] = tuple(left_bounds)
            if not restrict_used:
                # if restrict has not been used to set a coordinate bound
                # it is maintained in the list of restrictions:
                new_restrictions.append(restrict)
        self._bounds = tuple(bounds)
        self._restrictions = new_restrictions

    def restrict(self, subset, restrictions=None):
        r"""
        Return the restriction of the chart to some open subset of its domain.

        If the current chart is `(U,\varphi)`, a *restriction* (or *subchart*)
        is a chart `(V,\psi)` such that `V\subset U` and `\psi = \varphi |_V`.

        If such subchart has not been defined yet, it is constructed here.

        The coordinates of the subchart bare the same names as the coordinates
        of the current chart.

        INPUT:

        - ``subset`` -- open subset `V` of the chart domain `U` (must be an
          instance of :class:`~sage.manifolds.manifold.TopologicalManifold`)
        - ``restrictions`` -- (default: ``None``) list of coordinate
          restrictions defining the subset `V`

        A restriction can be any symbolic equality or inequality involving
        the coordinates, such as ``x > y`` or ``x^2 + y^2 != 0``. The items
        of the list ``restrictions`` are combined with the ``and`` operator;
        if some restrictions are to be combined with the ``or`` operator
        instead, they have to be passed as a tuple in some single item
        of the list ``restrictions``. For example::

          restrictions = [x > y, (x != 0, y != 0), z^2 < x]

        means (``x > y``) and ((``x != 0``) or (``y != 0``)) and
        (``z^2 < x``). If the list ``restrictions`` contains only one
        item, this item can be passed as such, i.e. writing ``x > y``
        instead of the single element list ``[x > y]``.

        OUTPUT:

        - chart `(V,\psi)`, as an instance of :class:`RealChart`.

        EXAMPLES:

        Cartesian coordinates on the unit open disc in `\RR^2` as a subchart
        of the global Cartesian coordinates::

            sage: M = Manifold(2, 'R^2', structure='topological')
            sage: c_cart.<x,y> = M.chart() # Cartesian coordinates on R^2
            sage: D = M.open_subset('D') # the unit open disc
            sage: c_cart_D = c_cart.restrict(D, x^2+y^2<1)
            sage: p = M.point((1/2, 0))
            sage: p in D
            True
            sage: q = M.point((1, 2))
            sage: q in D
            False

        Cartesian coordinates on the annulus `1 < \sqrt{x^2+y^2} < 2`::

            sage: A = M.open_subset('A')
            sage: c_cart_A = c_cart.restrict(A, [x^2+y^2>1, x^2+y^2<4])
            sage: p in A, q in A
            (False, False)
            sage: a = M.point((3/2,0))
            sage: a in A
            True

        """
        if subset == self._domain:
            return self
        if subset not in self._dom_restrict:
            if not subset.is_subset(self._domain):
                raise ValueError("the specified subset is not a subset " +
                                 "of the domain of definition of the chart")
            coordinates = ""
            for coord in self._xx:
                coordinates += repr(coord) + ' '
            res = type(self)(subset, coordinates)
            res._bounds = self._bounds
            res._restrictions.extend(self._restrictions)
            # The coordinate restrictions are added to the result chart and
            # possibly transformed into coordinate bounds:
            if restrictions is not None:
                res.add_restrictions(restrictions)
            # Update of supercharts and subcharts:
            res._supercharts.update(self._supercharts)
            for schart in self._supercharts:
                schart._subcharts.add(res)
                schart._dom_restrict[subset] = res
            # Update of domain restrictions:
            self._dom_restrict[subset] = res
        return self._dom_restrict[subset]

    def valid_coordinates(self, *coordinates, **kwds):
        r"""
        Check whether a tuple of coordinates can be the coordinates of a
        point in the chart domain.

        INPUT:

        - ``*coordinates`` -- coordinate values
        - ``**kwds`` -- options:

          - ``tolerance=0``, to set the absolute tolerance in the test of
            coordinate ranges
          - ``parameters=None``, to set some numerical values to parameters


        OUTPUT:

        - ``True`` if the coordinate values are admissible in the chart range
          and ``False`` otherwise

        EXAMPLES:

        Cartesian coordinates on a square interior::

            sage: forget()  # for doctest only
            sage: M = Manifold(2, 'M', structure='topological')  # the square interior
            sage: X.<x,y> = M.chart('x:(-2,2) y:(-2,2)')
            sage: X.valid_coordinates(0,1)
            True
            sage: X.valid_coordinates(-3/2,5/4)
            True
            sage: X.valid_coordinates(0,3)
            False

        The unit open disk inside the square::

            sage: D = M.open_subset('D', coord_def={X: x^2+y^2<1})
            sage: XD = X.restrict(D)
            sage: XD.valid_coordinates(0,1)
            False
            sage: XD.valid_coordinates(-3/2,5/4)
            False
            sage: XD.valid_coordinates(-1/2,1/2)
            True
            sage: XD.valid_coordinates(0,0)
            True

        """
        n = len(coordinates)
        if n != self._manifold._dim:
            return False
        if 'tolerance' in kwds:
            tolerance = kwds['tolerance']
        else:
            tolerance = 0
        if 'parameters' in kwds:
            parameters = kwds['parameters']
        else:
            parameters = None
        # Check of the coordinate ranges:
        for x, bounds in zip(coordinates, self._bounds):
            xmin = bounds[0][0] - tolerance
            min_included = bounds[0][1]
            xmax = bounds[1][0] + tolerance
            max_included = bounds[1][1]
            if parameters:
                xmin = xmin.subs(parameters)
                xmax = xmax.subs(parameters)
            if min_included:
                if x < xmin:
                    return False
            else:
                if x <= xmin:
                    return False
            if max_included:
                if x > xmax:
                    return False
            else:
                if x >= xmax:
                    return False
        # Check of additional restrictions:
        if self._restrictions != []:
            substitutions = dict(zip(self._xx, coordinates))
            if parameters:
                substitutions.update(parameters)
            for restrict in self._restrictions:
                if isinstance(restrict, tuple): # case of or conditions
                    combine = False
                    for expr in restrict:
                        combine = combine or bool(expr.subs(substitutions))
                    if not combine:
                        return False
                else:
                    if not bool(restrict.subs(substitutions)):
                        return False
        # All tests have been passed:
        return True


#*****************************************************************************

class CoordChange(SageObject):
    r"""
    Transition map between two charts of a topological manifold.

    Giving two coordinate charts `(U, \varphi)` and `(V, \psi)` on a
    topological manifold `M` of dimension `n` over a topological field `K`,
    the *transition map from* `(U, \varphi)` *to* `(V, \psi)` is the map

    .. MATH::

        \psi\circ\varphi^{-1}: \varphi(U\cap V) \subset K^n
        \rightarrow \psi(U\cap V) \subset K^n.

    In other words, the transition map `\psi \circ \varphi^{-1}` expresses
    the coordinates `(y^1, \ldots, y^n)` of `(V, \psi)` in terms of the
    coordinates `(x^1, \ldots, x^n)` of `(U, \varphi)` on the open subset
    where the two charts intersect, i.e. on `U \cap V`.

    INPUT:

    - ``chart1`` -- chart `(U, \varphi)`
    - ``chart2`` -- chart `(V, \psi)`
    - ``transformations`` -- tuple (or list) `(Y_1, \ldots, Y_2)`, where
      `Y_i` is the symbolic expression of the coordinate `y^i` in terms
      of the coordinates `(x^1, \ldots, x^n)`

    EXAMPLES:

    Transition map on a 2-dimensional topological manifold::

        sage: M = Manifold(2, 'M', structure='topological')
        sage: X.<x,y> = M.chart()
        sage: Y.<u,v> = M.chart()
        sage: X_to_Y = X.transition_map(Y, [x+y, x-y])
        sage: X_to_Y
        Change of coordinates from Chart (M, (x, y)) to Chart (M, (u, v))
        sage: type(X_to_Y)
        <class 'sage.manifolds.chart.CoordChange'>
        sage: X_to_Y.display()
        u = x + y
        v = x - y

    """
    def __init__(self, chart1, chart2, *transformations):
        r"""
        Construct a transition map.

        TESTS::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: Y.<u,v> = M.chart()
            sage: X_to_Y = X.transition_map(Y, [x+y, x-y])
            sage: X_to_Y
            Change of coordinates from Chart (M, (x, y)) to Chart (M, (u, v))
            sage: type(X_to_Y)
            <class 'sage.manifolds.chart.CoordChange'>
            sage: TestSuite(X_to_Y).run()

        """
        self._n1 = len(chart1._xx)
        self._n2 = len(chart2._xx)
        if len(transformations) != self._n2:
            raise ValueError("{} coordinate transformations ".format(self._n2)
                             + "must be provided")
        self._chart1 = chart1
        self._chart2 = chart2
        #*# when MultiCoordFunction will be implemented (trac #18640):
        # self._transf = chart1.multifunction(*transformations)
        #*# for now:
        self._transf = transformations
        self._inverse = None
        # If the two charts are on the same open subset, the coordinate change
        # is added to the subset (and supersets) dictionary:
        if chart1._domain == chart2._domain:
            domain = chart1._domain
            for sdom in domain._supersets:
                sdom._coord_changes[(chart1, chart2)] = self

    def _repr_(self):
        r"""
        String representation of the transition map.

        TESTS::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: Y.<u,v> = M.chart()
            sage: X_to_Y = X.transition_map(Y, [x+y, x-y])
            sage: X_to_Y._repr_()
            'Change of coordinates from Chart (M, (x, y)) to Chart (M, (u, v))'
            sage: repr(X_to_Y)  # indirect doctest
            'Change of coordinates from Chart (M, (x, y)) to Chart (M, (u, v))'
            sage: X_to_Y  # indirect doctest
            Change of coordinates from Chart (M, (x, y)) to Chart (M, (u, v))

        """
        return "Change of coordinates from {} to {}".format(self._chart1,
                                                            self._chart2)

    def _latex_(self):
        r"""
        LaTeX representation of the transition map.

        TESTS::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: Y.<u,v> = M.chart()
            sage: X_to_Y = X.transition_map(Y, [x+y, x-y])
            sage: X_to_Y._latex_()
            \left(M,(x, y)\right) \rightarrow \left(M,(u, v)\right)
            sage: latex(X_to_Y)  # indirect doctest
            \left(M,(x, y)\right) \rightarrow \left(M,(u, v)\right)

        """
        return latex(self._chart1) + r' \rightarrow ' + latex(self._chart2)

    def __eq__(self, other):
        r"""
        Equality operator.

        TESTS::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: Y.<u,v> = M.chart()
            sage: X_to_Y = X.transition_map(Y, [x+y, x-y])
            sage: X_to_Y == X_to_Y
            True
            sage: X_to_Y1 = X.transition_map(Y, [x+y, x-y])
            sage: X_to_Y == X_to_Y1
            True
            sage: X_to_Y2 = X.transition_map(Y, [2*y, -x])
            sage: X_to_Y == X_to_Y2
            False
            sage: Z.<w,z> = M.chart()
            sage: X_to_Z = X.transition_map(Z, [x+y, x-y])
            sage: X_to_Y == X_to_Z
            False

        """
        if other is self:
            return True
        if not isinstance(other, CoordChange):
            return False
        return ((self._chart1 == other._chart1)
                and (self._chart2 == other._chart2)
                and (self._transf == other._transf))

    def __ne__(self, other):
        r"""
        Unequality operator.

        TESTS::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: Y.<u,v> = M.chart()
            sage: X_to_Y = X.transition_map(Y, [x+y, x-y])
            sage: X_to_Y2 = X.transition_map(Y, [2*y, -x])
            sage: X_to_Y != X_to_Y2
            True

        """
        return not (self == other)

    def __call__(self, *coords):
        r"""
        Compute the new coordinates from old ones.

        INPUT:

        - ``coords`` -- values of coordinates of ``chart1``

        OUTPUT:

        - tuple of values of coordinates of ``chart2``

        EXAMPLES::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: Y.<u,v> = M.chart()
            sage: X_to_Y = X.transition_map(Y, [x+y, x-y])
            sage: X_to_Y(1,2)
            (3, -1)

        """
        #*# When MultiCoordFunction is implemented (trac #18640):
        # return self._transf(*coords)
        #*# for now:
        substitutions = {self._chart1._xx[j]: coords[j] for j in range(self._n1)}
        return tuple([self._transf[i].subs(substitutions).simplify_full()
                      for i in range(self._n2)])

    def inverse(self):
        r"""
        Compute the inverse coordinate transformation.

        OUTPUT:

        - an instance of :class:`CoordChange` representing the inverse of
          the current coordinate transformation

        EXAMPLES:

        Inverse of a coordinate transformation corresponding to a
        `\pi/3`-rotation in the plane::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: c_xy.<x,y> = M.chart()
            sage: c_uv.<u,v> = M.chart()
            sage: xy_to_uv = c_xy.transition_map(c_uv, ((x - sqrt(3)*y)/2, (sqrt(3)*x + y)/2))
            sage: M.coord_changes()
            {(Chart (M, (x, y)),
              Chart (M, (u, v))): Change of coordinates from Chart (M, (x, y)) to Chart (M, (u, v))}
            sage: uv_to_xy = xy_to_uv.inverse(); uv_to_xy
            Change of coordinates from Chart (M, (u, v)) to Chart (M, (x, y))
            sage: uv_to_xy.display()
            x = 1/2*sqrt(3)*v + 1/2*u
            y = -1/2*sqrt(3)*u + 1/2*v
            sage: M.coord_changes()  # random (dictionary output)
            {(Chart (M, (u, v)),
              Chart (M, (x, y))): Change of coordinates from Chart (M, (u, v)) to Chart (M, (x, y)),
             (Chart (M, (x, y)),
              Chart (M, (u, v))): Change of coordinates from Chart (M, (x, y)) to Chart (M, (u, v))}

        """
        from sage.symbolic.relation import solve
        if self._inverse is not None:
            return self._inverse
        # The computation is necessary:
        x1 = self._chart1._xx  # list of coordinates in chart1
        x2 = self._chart2._xx  # list of coordinates in chart2
        n1 = self._n1
        n2 = self._n2
        if n1 != n2:
            raise ValueError("the change of coordinates is not invertible " +
                             "(different number of coordinates in the two " +
                             "charts)")
        # New symbolic variables (different from x2 to allow for a
        #  correct solution even when chart2 = chart1):
        base_field = self._chart1.domain().base_field_type()
        if base_field == 'real':
            coord_domain = ['real' for i in range(n2)]
        elif base_field == 'complex':
            coord_domain = ['complex' for i in range(n2)]
        else:
            coord_domain = [None for i in range(n2)]
        for i in range(n2):
            if x2[i].is_positive():
                coord_domain[i] = 'positive'
        xp2 = [ SR.var('xxxx' + str(i), domain=coord_domain[i])
                for i in range(n2) ]
        #*# when MultiCoordFunction will be implemented (trac #18640):
        # xx2 = self._transf.expr()
        #*# for now:
        xx2 = self._transf
        equations = [xp2[i] == xx2[i] for i in range(n2)]
        try:
            solutions = solve(equations, *x1, solution_dict=True)
        except RuntimeError:
            raise RuntimeError("the system could not be solved; use " +
                               "set_inverse() to set the inverse manually")
        substitutions = dict(zip(xp2, x2))
        if len(solutions) == 1:
            x2_to_x1 = [solutions[0][x1[i]].subs(substitutions)
                                                            for i in range(n1)]
        else:
            list_x2_to_x1 = []
            for sol in solutions:
                if x2[0] in sol:
                    raise ValueError("the system could not be solved; use " +
                                     "set_inverse() to set the inverse " +
                                     "manually")
                x2_to_x1 = [sol[x1[i]].subs(substitutions) for i in range(n1)]
                if self._chart1.valid_coordinates(*x2_to_x1):
                    list_x2_to_x1.append(x2_to_x1)
            if len(list_x2_to_x1) == 0:
                raise ValueError("no solution found; use set_inverse() to " +
                                 "set the inverse manually")
            if len(list_x2_to_x1) > 1:
                print "Multiple solutions found: "
                print list_x2_to_x1
                raise ValueError(
                   "non-unique solution to the inverse coordinate " +
                   "transformation; use set_inverse() to set the inverse " +
                   "manually")
            x2_to_x1 = list_x2_to_x1[0]
        self._inverse = type(self)(self._chart2, self._chart1, *x2_to_x1)
        return self._inverse

    def set_inverse(self, *transformations, **kwds):
        r"""
        Sets the inverse of the coordinate transformation.

        This is useful when the automatic computation via :meth:`inverse()`
        fails.

        INPUT:

        - ``transformations`` -- the inverse transformations expressed as a
          list of the expressions of the "old" coordinates in terms of the
          "new" ones
        - ``kwds`` -- keyword arguments: only ``verbose=True`` or
          ``verbose=False`` (default) are meaningful; it determines whether
          the provided transformations are checked to be indeed the inverse
          coordinate transformations

        EXAMPLES:

        From spherical coordinates to Cartesian ones in the plane::

            sage: M = Manifold(2, 'R^2', structure='topological')
            sage: U = M.open_subset('U') # the complement of the half line {y=0, x>= 0}
            sage: c_cart.<x,y> = U.chart()
            sage: c_spher.<r,ph> = U.chart(r'r:(0,+oo) ph:(0,2*pi):\phi')
            sage: spher_to_cart = c_spher.transition_map(c_cart, [r*cos(ph), r*sin(ph)])
            sage: spher_to_cart.set_inverse(sqrt(x^2+y^2), atan2(y,x))
            sage: spher_to_cart.inverse()
            Change of coordinates from Chart (U, (x, y)) to Chart (U, (r, ph))
            sage: spher_to_cart.inverse().display()
            r = sqrt(x^2 + y^2)
            ph = arctan2(y, x)
            sage: M.coord_changes()  # random (dictionary output)
            {(Chart (U, (r, ph)),
              Chart (U, (x, y))): Change of coordinates from Chart (U, (r, ph)) to Chart (U, (x, y)),
             (Chart (U, (x, y)),
              Chart (U, (r, ph))): Change of coordinates from Chart (U, (x, y)) to Chart (U, (r, ph))}

        Introducing a wrong inverse transformation (note the ``x^3`` typo) is
        revealed by setting ``verbose`` to ``True``::

            sage: spher_to_cart.set_inverse(sqrt(x^3+y^2), atan2(y,x), verbose=True)
            Check of the inverse coordinate transformation:
               r == sqrt(r^3*cos(ph)^3 + r^2*sin(ph)^2)
               ph == arctan2(r*sin(ph), r*cos(ph))
               x == sqrt(x^3 + y^2)*x/sqrt(x^2 + y^2)
               y == sqrt(x^3 + y^2)*y/sqrt(x^2 + y^2)

        """
        verbose = kwds.get('verbose', False)
        self._inverse = type(self)(self._chart2, self._chart1,
                                   *transformations)
        if verbose:
            print("Check of the inverse coordinate transformation:")
            x1 = self._chart1._xx
            x2 = self._chart2._xx
            n1 = len(x1)
            for i in range(n1):
                print("  {} == {}".format(x1[i], self._inverse(*(self(*x1)))[i]))
            for i in range(n1):
                print("  {} == {}".format(x2[i], self(*(self._inverse(*x2)))[i]))

    def __mul__(self, other):
        r"""
        Composition with another change of coordinates.

        INPUT:

        - ``other`` -- another change of coordinate, the final chart of
          it is the initial chart of ``self``

        OUTPUT:

        - the change of coordinates `X_1 \to X_3`, where `X_1` is the initial
          chart of ``other`` and `X_3` is the final chart of ``self``

        EXAMPLES::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: U.<u,v> = M.chart()
            sage: X_to_U = X.transition_map(U, (x+y, x-y))
            sage: W.<w,z> = M.chart()
            sage: U_to_W = U.transition_map(W, (u+cos(u)/2, v-sin(v)/2))
            sage: X_to_W = U_to_W * X_to_U; X_to_W
            Change of coordinates from Chart (M, (x, y)) to Chart (M, (w, z))
            sage: X_to_W.display()
            w = 1/2*cos(x)*cos(y) - 1/2*sin(x)*sin(y) + x + y
            z = -1/2*cos(y)*sin(x) + 1/2*cos(x)*sin(y) + x - y

        """
        if not isinstance(other, CoordChange):
            raise TypeError("{} is not a change of coordinate".format(other))
        if other._chart2 != self._chart1:
            raise ValueError("composition not possible: " +
                             "{} is different from {}".format(other._chart2,
                                                              other._chart1))
        #*# when MultiCoordFunction will be implemented (trac #18640):
        # transf = self._transf(*(other._transf.expr()))
        #*# for now:
        transf = self(*(other._transf))
        return type(self)(other._chart1, self._chart2, *transf)

    def restrict(self, dom1, dom2=None):
        r"""
        Restriction to subsets.

        INPUT:

        - ``dom1`` -- open subset of the domain of ``chart1``
        - ``dom2`` -- (default: ``None``) open subset of the domain of
          ``chart2``; if ``None``, ``dom1`` is assumed

        OUTPUT:

        - the transition map between the charts restricted to the
          specified subsets

        EXAMPLES::

            sage: M = Manifold(2, 'M', structure='topological')
            sage: X.<x,y> = M.chart()
            sage: Y.<u,v> = M.chart()
            sage: X_to_Y = X.transition_map(Y, [x+y, x-y])
            sage: U = M.open_subset('U', coord_def={X: x>0, Y: u+v>0})
            sage: X_to_Y_U = X_to_Y.restrict(U); X_to_Y_U
            Change of coordinates from Chart (U, (x, y)) to Chart (U, (u, v))
            sage: X_to_Y_U.display()
            u = x + y
            v = x - y

        The result is cached::

            sage: X_to_Y.restrict(U) is X_to_Y_U
            True

        """
        if dom2 is None:
            dom2 = dom1
        ch1 = self._chart1.restrict(dom1)
        ch2 = self._chart2.restrict(dom2)
        if (ch1, ch2) in dom1.coord_changes():
            return dom1.coord_changes()[(ch1,ch2)]
        #*# when MultiCoordFunction will be implemented (trac #18640):
        # return type(self)(self._chart1.restrict(dom1),
        #                   self._chart2.restrict(dom2), *(self._transf.expr()))
        #*# for now:
        return type(self)(self._chart1.restrict(dom1),
                           self._chart2.restrict(dom2), *(self._transf))

    def display(self):
        r"""
        Display of the coordinate transformation.

        The output is either text-formatted (console mode) or LaTeX-formatted
        (notebook mode).

        EXAMPLES:

        From spherical coordinates to Cartesian ones in the plane::

            sage: M = Manifold(2, 'R^2', structure='topological')
            sage: U = M.open_subset('U') # the complement of the half line {y=0, x>= 0}
            sage: c_cart.<x,y> = U.chart()
            sage: c_spher.<r,ph> = U.chart(r'r:(0,+oo) ph:(0,2*pi):\phi')
            sage: spher_to_cart = c_spher.transition_map(c_cart, [r*cos(ph), r*sin(ph)])
            sage: spher_to_cart.display()
            x = r*cos(ph)
            y = r*sin(ph)
            sage: latex(spher_to_cart.display())
            \left\{\begin{array}{lcl} x & = & r \cos\left({\phi}\right) \\
             y & = & r \sin\left({\phi}\right) \end{array}\right.

        A shortcut is ``disp()``::

            sage: spher_to_cart.disp()
            x = r*cos(ph)
            y = r*sin(ph)

        """
        from sage.misc.latex import latex
        from sage.tensor.modules.format_utilities import FormattedExpansion
        coords2 = self._chart2[:]
        n2 = len(coords2)
        #*# when MultiCoordFunction will be implemented (trac #18640):
        # expr = self._transf.expr()
        #*# for now:
        expr = self._transf
        rtxt = ""
        if n2 == 1:
            rlatex = r"\begin{array}{lcl}"
        else:
            rlatex = r"\left\{\begin{array}{lcl}"
        for i in range(n2):
            x2 = coords2[i]
            x2f = expr[i]
            rtxt += repr(x2) + " = " + repr(x2f) + "\n"
            rlatex += latex(x2) + r" & = & " + latex(x2f) + r"\\"
        rtxt = rtxt[:-1]  # remove the last new line
        rlatex = rlatex[:-2] + r"\end{array}"
        if n2 > 1:
            rlatex += r"\right."
        return FormattedExpansion(rtxt, rlatex)

    disp = display
