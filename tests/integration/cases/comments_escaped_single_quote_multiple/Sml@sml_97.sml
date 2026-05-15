datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("host", SStr "it's here"),  (* a comment *)
    ("port", SInt 80)  (* another *)
]
val _ = my_data
