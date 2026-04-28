datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    (* line 1 *)
    (* line 2 *)
    SStr "a"
]
val _ = my_data
