module [my_data]

JsonVal : [
    RFloat F64,
    RList (List JsonVal),
]

my_data : JsonVal
my_data = RList [
    RFloat 1.1,
    RFloat -2.2,
    RFloat 3.3,
    ]
