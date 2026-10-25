datatype val_t =
    SReal of real
  | SStr of string
  | SDate of (int * int * int)
  | SInt of LargeInt.int
  | SList of val_t list
fun capture _ = ()
val _ = capture(SReal ((0.0 / 0.0)), SReal ((1.0 / 0.0)), SReal ((~1.0 / 0.0)), SReal 1.25, SDate (2024, 1, 15), SInt 1705322096, SStr "[ordinary text]")
