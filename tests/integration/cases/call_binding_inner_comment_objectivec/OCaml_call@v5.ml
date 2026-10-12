module Check = struct

let make_widget _ = ()
type val_t =
  | OInt of int
let my_data = make_widget(OInt 42) ?
make_widget(OInt 42) // inner
: nil // trailing

end
