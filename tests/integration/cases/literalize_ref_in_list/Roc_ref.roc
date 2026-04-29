module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

val_x : Val
val_y : Val
val_x = RDict [
    ("_", RStr "_"),
    ]
val_y = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = RList [
    val_x,
    val_y,
    ]
