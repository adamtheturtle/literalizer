module Check = struct

let shared : Yojson.Safe.t = `Assoc [
    ("field", `List [`Int 1; `Int 2])
]
let my_data : Yojson.Safe.t = shared

end
