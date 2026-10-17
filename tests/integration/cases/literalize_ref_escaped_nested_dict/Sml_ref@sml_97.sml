datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val existing : val_t = SInt 1
val my_data : val_t = SMap [
    ("nested", SList [SInt 0, existing])
]
val _ = my_data
