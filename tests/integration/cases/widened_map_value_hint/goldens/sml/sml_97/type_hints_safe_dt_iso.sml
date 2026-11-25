datatype val_t =
    SNull
  | SBool of bool
  | SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("a", SInt 1)],
    SInt 1,
    SStr "x",
    SBool true,
    SReal 2.5,
    SNull
]
val _ = my_data
