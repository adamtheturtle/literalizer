datatype val_t =
    SNull
  | SBool of bool
  | SReal of real
  | SDate of (int * int * int)
  | SDatetime of ((int * int * int) * (int * int * int))
  | SList of val_t list
val my_data : val_t = SList [
    SBool true,
    SReal 1.5,
    SNull,
    SDate (2020, 1, 1),
    SDatetime ((2020, 1, 1), (0, 0, 0)),
    SList []
]
val _ = my_data
