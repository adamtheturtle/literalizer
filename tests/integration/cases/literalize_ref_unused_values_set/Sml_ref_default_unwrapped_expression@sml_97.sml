datatype val_t =
    SInt of LargeInt.int
  | SSet of val_t list
fun consume_widget _ = ()
val _ = consume_widget(SSet [
    SInt 1,
    SInt 2
])
