module Check = struct

let make_widget _ = ()
type val_t =
  | OInt of int
let my_data = ($"{(true ? "// payload" : "ok")}").Length >= 0 ? make_widget(OInt 42) : make_widget(OInt 42) // trailing
// extra

end
