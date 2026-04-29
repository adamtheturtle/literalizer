datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val x : val_t = SInt 0
val y : val_t = SInt 0
val my_data : val_t = SList [
    x,
    y
]
val _ = my_data
