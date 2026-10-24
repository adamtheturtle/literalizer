datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val std : val_t = SMap [
    ("a", SInt 1)
]
val arena : val_t = SMap [
    ("a", SInt 1)
]
val allocator : val_t = SMap [
    ("a", SInt 1)
]
val my_data : val_t = SList [
    std,
    arena,
    allocator
]
val _ = my_data
