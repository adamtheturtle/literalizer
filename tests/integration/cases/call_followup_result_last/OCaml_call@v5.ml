module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let make_widget _ = ()
let consume _ = ()
let my_data = make_widget(OInt 42, OInt 3)
let _ = consume(OInt 3, my_data)

end
