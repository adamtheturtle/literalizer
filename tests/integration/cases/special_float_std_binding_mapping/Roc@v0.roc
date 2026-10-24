module [std]

Val : [
    RFloat F64,
    RStr Str,
    RDict (List (Str, Val)),
]

std : Val
std = RDict [
    ("nan", RFloat Num.nan_f64),
    ("positive", RFloat Num.infinity_f64),
    ("negative", RFloat -Num.infinity_f64),
]
