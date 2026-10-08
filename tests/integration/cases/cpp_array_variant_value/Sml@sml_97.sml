datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SInt 1),
    ("b", SStr "x"),
    ("e", SList [SInt 1, SInt 2]),
    ("f", SMap [("g", SStr "h")])
]
val _ = my_data
