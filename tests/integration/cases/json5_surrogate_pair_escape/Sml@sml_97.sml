datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("astral", SStr "\240\159\152\128"),
    ("mixed", SStr "a\240\159\152\128b"),
    ("count", SInt 2),
    ("list", SList [SStr "\240\159\152\128", SInt 1]),
    ("nested", SMap [("inner", SStr "\240\159\152\128")])
]
val _ = my_data
