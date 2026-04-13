structure Check = struct

datatype val_t =
    SNull
  | SBool of bool
  | SInt of int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("name", SStr "Alice"),
    ("age", SInt 30),
    ("active", SBool true),
    ("score", SNull)
]

end
