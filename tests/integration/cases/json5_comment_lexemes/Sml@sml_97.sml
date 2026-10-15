datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* heading *)
    ("a", SStr "single ' // data"),
    ("b", SStr "linecontinuation"),
    ("c", SStr "\\"),  (* actual comment *)
    ("d", SStr "\226\128\168\226\128\169")  (* final comment *)
]
val _ = my_data
