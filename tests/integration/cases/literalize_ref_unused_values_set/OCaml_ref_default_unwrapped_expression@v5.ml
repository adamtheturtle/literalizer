module Check = struct

type val_t =
  | OInt of int
  | OSet of val_t list
let consume_widget _ = ()
let _ = consume_widget(OSet [
    OInt 1;
    OInt 2
])

end
