module Check = struct

let make_widget _ = ()
type val_t =
  | OStr of string
let my_data = make_widget(OStr "first \"quote\"\n// string body") // note
// extra

end
