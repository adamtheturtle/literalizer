module Check = struct

type val_t =
  | ONull
  | OInt of int
let make_widget _ = ()
let my_data = make_widget(ONull)
let my_data = ($"{$"{1://}"}").Length >= 0 ? make_widget(OInt 42) : make_widget(OInt 42) // trailing
// extra

end
