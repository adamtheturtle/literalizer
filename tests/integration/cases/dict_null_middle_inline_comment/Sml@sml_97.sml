datatype val_t =
    SNull
  | SBool of bool
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("server", SMap [
        ("host", SStr "localhost"),
        ("port", SNull),  (* not configured yet *)
        ("debug", SBool true)
    ])
]
val _ = my_data
