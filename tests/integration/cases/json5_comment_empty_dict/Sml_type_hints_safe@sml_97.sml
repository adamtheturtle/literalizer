datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
(* empty heading *)
(* empty body *)
(* after empty *)
val my_data : val_t = SMap []
val _ = my_data
