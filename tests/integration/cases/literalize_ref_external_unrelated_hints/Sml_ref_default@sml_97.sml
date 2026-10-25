datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun consume_widget _ = ()
val missing : val_t = SList [
    SInt 1,
    SInt 2
]
val my_data : val_t = missing
val _ = consume_widget(my_data)
