datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun consume_widget _ = ()
val shared : val_t = SList [
    SInt 1,
    SInt 2
]
val my_data : val_t = shared
val _ = consume_widget(my_data)
