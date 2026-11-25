datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* before	line *)
    ("value", SStr "left\tright")  (* inline	line *)
    (* after	line *)
]
val _ = my_data
