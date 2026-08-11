datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
fun consume _ = ()
val foo : val_t = SInt 42
val _ = consume(SList [
    SMap [
        ("other", SInt 1)
    ],
    foo
], SMap [
    ("left", foo),
    ("other", SInt 1)
])
