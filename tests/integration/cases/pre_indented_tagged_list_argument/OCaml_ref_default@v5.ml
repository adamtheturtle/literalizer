module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let consume_widget _ = ()
let _ = consume_widget(    OList [
        OInt 1;
        OInt 2
    ])

end
