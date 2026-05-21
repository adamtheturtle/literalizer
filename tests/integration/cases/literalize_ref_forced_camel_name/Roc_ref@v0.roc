module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

userObj : Val
userObj = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = userObj
