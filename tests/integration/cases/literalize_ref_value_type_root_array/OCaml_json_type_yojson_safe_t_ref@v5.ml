module Check = struct

let shared : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let my_data : Yojson.Safe.t = shared

end
