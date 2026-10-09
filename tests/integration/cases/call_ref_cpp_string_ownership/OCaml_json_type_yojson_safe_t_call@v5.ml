module Check = struct

let consume _ = ()
let item : Yojson.Safe.t = `String "s"
let _ = consume(item)

end
