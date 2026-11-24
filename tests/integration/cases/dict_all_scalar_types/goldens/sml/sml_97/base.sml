datatype val_t =
    SNull
  | SBool of bool
  | SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SDate of (int * int * int)
  | SDatetime of ((int * int * int) * (int * int * int))
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("s", SStr "string"),
    ("i", SInt 1),
    ("f", SReal 1.5),
    ("b", SBool true),
    ("n", SNull),
    ("d", SDate (2024, 1, 15)),
    ("dt", SDatetime ((2024, 1, 15), (12, 0, 0))),
    ("by", SStr "48656c6c6f")
]
val _ = my_data
