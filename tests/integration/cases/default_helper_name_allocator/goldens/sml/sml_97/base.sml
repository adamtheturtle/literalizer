datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val allocator : val_t = SMap [
    ("a", SInt 1)
]
val _ = allocator
