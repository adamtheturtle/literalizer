module Check = struct

let make_widget _ = ()
type val_t =
  | OInt of int
let result : val_t = OInt make_widget(42)

end
