structure Check = struct

datatype val_t =
    SInt of int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SMap [("x", SInt 1)]),
    ("b", SInt 2)
]

end
