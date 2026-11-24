module Check = struct

let consume _ = ()
let shared : Yojson.Safe.t = `Int 42
let _ = consume(`List [shared; shared])

end
