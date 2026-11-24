module Check = struct

let shared : Yojson.Safe.t = `Int 42
let my_data : Yojson.Safe.t = `List [
    shared;
    shared
]

end
