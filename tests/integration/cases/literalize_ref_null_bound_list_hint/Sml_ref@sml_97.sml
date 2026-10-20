datatype val_t =
    SNull
  | SInt of LargeInt.int
  | SList of val_t list
val my_value : val_t = SNull
val my_data : val_t = my_value
val _ = my_data
