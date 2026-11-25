datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun consume_widget _ = ()
val a : val_t = SInt 0
val my_data : val_t = SList [
    a,
    SInt 1
]
val _ = consume_widget(my_data)
