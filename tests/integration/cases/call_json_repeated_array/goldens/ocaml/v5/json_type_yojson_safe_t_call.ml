module Check = struct

let consume _ = ()
let shared : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let _ = consume(`List [shared; shared])

end
