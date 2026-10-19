datatype val_t =
    SInt of LargeInt.int
  | SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SInt (~42),
    SInt 0,
    SInt 42,
    SReal (~1.250000),
    SReal 0.000000,
    SReal 1.250000
]
val _ = my_data
