datatype val_t =
    SDatetime of ((int * int * int) * (int * int * int))
  | SList of val_t list
val my_data : val_t = SList [
    SDatetime ((2024, 1, 15), (12, 30, 0)),
    SDatetime ((2024, 6, 1), (8, 0, 0))
]
val _ = my_data
