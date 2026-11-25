datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("name", SStr "Alice"),
    ("scores", SList [
        SInt 10,
        SInt 20,
        SInt 30
    ])
]
val _ = my_data
