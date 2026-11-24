module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let consume_widget _ = ()
let a : val_t = OInt 0
let my_data : val_t = OList [
    a;
    OInt 1
]
let _ = consume_widget(my_data)

end
