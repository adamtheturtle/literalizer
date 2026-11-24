datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* first dotted key *)
    (* second dotted key *)
    ("a", SMap [("b", SInt 1), ("c", SInt 2)])
]
val _ = my_data
