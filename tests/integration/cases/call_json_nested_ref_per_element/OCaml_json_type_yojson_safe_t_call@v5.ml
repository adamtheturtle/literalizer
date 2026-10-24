module Check = struct

let consume _ = ()
let shared : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let _ = consume(`Assoc [("field", shared)])
let _ = consume(shared)

end
