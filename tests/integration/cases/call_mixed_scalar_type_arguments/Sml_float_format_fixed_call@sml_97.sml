datatype val_t =
    SReal of real
  | SStr of string
  | SDate of (int * int * int)
  | SDatetime of ((int * int * int) * (int * int * int))
  | SList of val_t list
fun capture _ = ()
val _ = capture(SReal ((0.0 / 0.0)), SReal ((1.0 / 0.0)), SReal ((~1.0 / 0.0)), SReal 1.250000, SDate (2024, 1, 15), SDatetime ((2024, 1, 15), (12, 34, 56)), SStr "[ordinary text]")
