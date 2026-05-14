datatype val_t =
    SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("x", SInt 1), ("y", SReal 2.5)],
    SMap [("x", SInt 3), ("y", SReal 4.0)]
]
val _ = my_data
