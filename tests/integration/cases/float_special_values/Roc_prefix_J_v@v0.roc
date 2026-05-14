module [my_data]

Val : [
    JFloat F64,
    JList (List Val),
]

my_data : Val
my_data = JList [
    JFloat Num.infinity_f64,
    JFloat -Num.infinity_f64,
    JFloat Num.nan_f64,
    ]
