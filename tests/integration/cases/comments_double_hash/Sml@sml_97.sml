datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    (* # section *)
    SStr "a"
]
val _ = my_data
