datatype val_t =
    SNull
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* null heading *)
    (* before null *)
    ("a", SNull),  (* first null *)
    ("b", SNull)  (* second null *)
]
val _ = my_data
