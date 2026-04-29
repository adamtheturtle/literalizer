module [my_data]

Val : [
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RFloat Num.infinity_f64,
    RFloat -Num.infinity_f64,
    RFloat Num.nan_f64,
    ]
