module Check = struct

let consume_widget _ = ()
let shared : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let my_data : Yojson.Safe.t = shared
let _ = consume_widget(my_data)

end
