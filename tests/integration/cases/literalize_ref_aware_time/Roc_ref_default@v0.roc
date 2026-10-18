module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

shared_time : Val
shared_time = RStr "12:30:15+02:00"
my_data : Val
my_data = RDict [
    ("x", shared_time),
]
