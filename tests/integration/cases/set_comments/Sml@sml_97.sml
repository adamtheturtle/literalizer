datatype val_t =
    SStr of string
  | SSet of val_t list
val my_data : val_t = SSet [
    SStr "apple",  (* inline comment *)
    (* before banana *)
    SStr "banana"
    (* trailing *)
]
val _ = my_data
