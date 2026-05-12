datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
  | SSet of val_t list
val my_data : val_t = SMap [
    ("name", SStr "Alice"),
    ("tags", SSet [
        SBool true,
        SInt 42,
        SStr "apple"
    ])
]
val _ = my_data
