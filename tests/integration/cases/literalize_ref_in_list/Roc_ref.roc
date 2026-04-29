val_x : Val
val_x = RDict [
    ("_", RStr "_"),
    ]
val_y : Val
val_y = RDict [
    ("_", RStr "_"),
    ]
module [my_data]

Val : [
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RList [
    val_x,
    val_y,
    ]
