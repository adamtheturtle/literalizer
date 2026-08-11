module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
    RInt 1i128,
    ]
