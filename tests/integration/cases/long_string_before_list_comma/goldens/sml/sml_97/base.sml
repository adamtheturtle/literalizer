datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
    SInt 1
]
val _ = my_data
