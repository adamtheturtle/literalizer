datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SReal 5.0E~324,
    SReal (~5.0E~324),
    SReal 1.0E~310
]
val _ = my_data
