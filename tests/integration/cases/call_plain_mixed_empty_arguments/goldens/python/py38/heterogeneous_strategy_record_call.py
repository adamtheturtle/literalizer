from typing import Union
def make_widget(before: 'Union[tuple[object, ...], tuple[str, ...]]', populated: 'Union[tuple[int, ...], tuple[str, ...]]', after: 'Union[tuple[object, ...], tuple[int, ...]]') -> object: ...
make_widget(before=(), populated=(1,), after=())
make_widget(before=("text",), populated=(2,), after=())
make_widget(before=(), populated=("text",), after=())
make_widget(before=("text",), populated=(2,), after=(3,))
