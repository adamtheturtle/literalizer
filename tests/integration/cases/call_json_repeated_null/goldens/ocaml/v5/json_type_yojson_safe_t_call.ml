module Check = struct

let consume _ = ()
let shared : Yojson.Safe.t = `Null
let _ = consume(`Assoc [("left", shared); ("nested", `List [shared])])

end
