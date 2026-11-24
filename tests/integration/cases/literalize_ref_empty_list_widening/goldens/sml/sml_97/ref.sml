datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val empty_values : val_t = SList []
val integer_values : val_t = SList [
    SInt 1
]
val my_data : val_t = SList [
    empty_values,
    integer_values
]
val _ = my_data
