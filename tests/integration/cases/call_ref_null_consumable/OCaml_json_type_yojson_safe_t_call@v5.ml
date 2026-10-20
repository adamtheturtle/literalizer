module Check = struct

let consume _ = ()
let my_null : Yojson.Safe.t = `Null
let regular_null : Yojson.Safe.t = `Null
let _ = consume(my_null)
let _ = consume(regular_null)

end
