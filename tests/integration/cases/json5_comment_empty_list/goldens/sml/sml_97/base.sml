datatype val_t =
    SList of val_t list
(* empty heading *)
(* empty body *)
(* after empty *)
val my_data : val_t = SList []
val _ = my_data
