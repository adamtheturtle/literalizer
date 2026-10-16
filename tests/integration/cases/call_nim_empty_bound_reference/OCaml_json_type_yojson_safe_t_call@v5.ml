module Check = struct

let make_widget _ = ()
let items : Yojson.Safe.t = `List []
let _ = make_widget(items)

end
