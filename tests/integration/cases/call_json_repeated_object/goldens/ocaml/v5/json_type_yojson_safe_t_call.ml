module Check = struct

let consume _ = ()
let shared : Yojson.Safe.t = `Assoc [
    ("value", `List [`Int 1; `Int 2])
]
let _ = consume(`Assoc [("left", shared); ("right", shared)])

end
