module Check = struct

let process _ = ()
let unknown_value : Yojson.Safe.t = `List []
let _ = process(`List [unknown_value])

end
