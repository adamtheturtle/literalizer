datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("if", SInt 1),
    ("then", SInt 2),
    ("else", SInt 3),
    ("let", SInt 4),
    ("in", SInt 5),
    ("using", SInt 6),
    ("missing", SInt 7),
    ("assert", SInt 8),
    ("as", SInt 9),
    ("Infinity", SInt 10),
    ("NaN", SInt 11),
    ("merge", SInt 12),
    ("Some", SInt 13),
    ("toMap", SInt 14),
    ("forall", SInt 15),
    ("with", SInt 16),
    ("ordinary", SInt 17)
]
val _ = my_data
