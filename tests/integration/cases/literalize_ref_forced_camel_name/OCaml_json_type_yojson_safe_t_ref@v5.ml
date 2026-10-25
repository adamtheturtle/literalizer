module Check = struct

let userObj : Yojson.Safe.t = `Assoc [
    ("_", `String "_")
]
let my_data : Yojson.Safe.t = userObj

end
