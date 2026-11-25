datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("assert", SInt 1),
    ("else", SInt 1),
    ("error", SInt 1),
    ("false", SInt 1),
    ("for", SInt 1),
    ("function", SInt 1),
    ("if", SInt 1),
    ("import", SInt 1),
    ("importbin", SInt 1),
    ("importstr", SInt 1),
    ("in", SInt 1),
    ("local", SInt 1),
    ("null", SInt 1),
    ("self", SInt 1),
    ("super", SInt 1),
    ("tailstrict", SInt 1),
    ("then", SInt 1),
    ("true", SInt 1),
    ("ordinary", SInt 1)
]
val _ = my_data
