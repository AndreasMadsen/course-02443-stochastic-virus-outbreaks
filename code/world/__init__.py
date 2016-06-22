
from .regions import regions, Region
from .routes import routes, Route
from ._cross_reference import cross_reference as _cross_reference
import tools

_cross_reference(regions, routes)
