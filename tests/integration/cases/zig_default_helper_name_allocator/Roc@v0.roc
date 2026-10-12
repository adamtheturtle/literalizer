module [allocator]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

allocator : Val
allocator = RDict [
    ("a", RInt 1i128),
]
