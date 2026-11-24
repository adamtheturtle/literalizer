datatype val_t =
    SDatetime of ((int * int * int) * (int * int * int))
  | SSet of val_t list
val my_data : val_t = SSet [
    SDatetime ((1901, 12, 13), (20, 45, 51)),
    SDatetime ((1901, 12, 13), (20, 45, 52)),
    SDatetime ((2038, 1, 19), (3, 14, 7)),
    SDatetime ((2038, 1, 19), (3, 14, 8))
]
val _ = my_data
