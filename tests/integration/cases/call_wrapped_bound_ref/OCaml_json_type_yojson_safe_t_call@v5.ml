module Check = struct

let make_widget _ = ()
let value : Yojson.Safe.t = `Int 1
let _ = make_widget(value)

end
