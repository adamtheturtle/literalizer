datatype val_t =
    SNull
  | SBool of bool
  | SReal of real
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("b", SNull),
    ("a", SMap [("y", SList [SReal 1.0]), ("x", SBool false)])
]
val _ = my_data
