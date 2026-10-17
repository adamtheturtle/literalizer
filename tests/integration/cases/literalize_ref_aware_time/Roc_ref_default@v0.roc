module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

value : Val
value = RStr "12:30:15+02:00"
my_data : Val
my_data = RDict [
    ("x", value),
]
