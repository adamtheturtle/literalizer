module [my_data]

JsonVal : [
    RFloat F64,
    RList (List JsonVal),
]

my_data : JsonVal
my_data = RList [
    RFloat Num.infinity_f64,
    RFloat -Num.infinity_f64,
    RFloat Num.nan_f64,
    ]
