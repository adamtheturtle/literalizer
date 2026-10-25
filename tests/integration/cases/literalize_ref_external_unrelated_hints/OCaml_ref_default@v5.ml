module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let consume_widget _ = ()
let missing : val_t = OList [
    OInt 1;
    OInt 2
]
let my_data : val_t = missing
let _ = consume_widget(my_data)

end
