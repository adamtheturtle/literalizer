from typing import Union
def make_widget(before: 'Union[list[object], list[str]]', populated: 'Union[list[int], list[str]]', after: 'Union[list[object], list[int]]') -> object: ...
make_widget(before=[], populated=[1], after=[])
make_widget(before=["text"], populated=[2], after=[])
make_widget(before=[], populated=["text"], after=[])
make_widget(before=["text"], populated=[2], after=[3])
