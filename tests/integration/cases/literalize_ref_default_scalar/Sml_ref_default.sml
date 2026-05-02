datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_var : val_t = SInt 1
val my_data : val_t = my_var
val _ = my_data
