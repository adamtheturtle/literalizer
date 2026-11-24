module Check = struct

type val_t =
  | OInt of int
let make_widget _ = ()
let value : val_t = OInt 1
let _ = make_widget(value)

end
