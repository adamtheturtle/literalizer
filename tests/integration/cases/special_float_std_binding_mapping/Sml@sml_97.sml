datatype val_t =
    SReal of real
  | SStr of string
  | SMap of (string * val_t) list
val std : val_t = SMap [
    ("nan", SReal ((0.0 / 0.0))),
    ("positive", SReal ((1.0 / 0.0))),
    ("negative", SReal ((~1.0 / 0.0)))
]
val _ = std
