module [my_data]

Val : [
    RFloat F64,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("pi", RFloat 3.141592653589793),
    ]
