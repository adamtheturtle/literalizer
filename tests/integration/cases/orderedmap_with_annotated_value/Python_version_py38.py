from typing import OrderedDict
from typing import Any, Tuple, Union
my_data: OrderedDict[str, Union[Tuple[Any, ...], int]] = OrderedDict([
    ("a", ()),
    ("b", 1),
])
