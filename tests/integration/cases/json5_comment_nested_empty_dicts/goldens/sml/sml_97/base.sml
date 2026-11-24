datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* outer heading *)
    (* first empty *)
    ("a", SMap []),
    (* second empty *)
    ("b", SMap [])
]
val _ = my_data
