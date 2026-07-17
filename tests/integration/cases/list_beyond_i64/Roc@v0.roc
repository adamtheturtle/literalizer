module [my_data]

Val : [
    RInt I128,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RInt 9223372036854775807i128,
    RInt 9223372036854775808i128,
    ]
