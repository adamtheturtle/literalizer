module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

std : Val
std = RDict [
    ("a", RInt 1i128),
]
arena : Val
arena = RDict [
    ("a", RInt 1i128),
]
allocator : Val
allocator = RDict [
    ("a", RInt 1i128),
]
my_data : Val
my_data = RList [
    std,
    arena,
    allocator,
]
