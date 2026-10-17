datatype val_t =
    SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("_", SList [SInt 1, SReal 2.5, SInt 3])
]
val _ = my_data
