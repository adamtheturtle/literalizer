module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

external_value : Val
external_value = RDict [
    ("_", RStr "_"),
]
my_data : Val
my_data = RList [
    external_value,
]
