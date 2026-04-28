module [my_data]

Val : [
    JNull,
    JBool Bool,
    JInt I128,
    JStr Str,
    JDict (List (Str, Val)),
]

my_data : Val
my_data = JDict [
    ("name", JStr "Alice"),
    ("age", JInt 30),
    ("active", JBool Bool.true),
    ("score", JNull),
    ]
