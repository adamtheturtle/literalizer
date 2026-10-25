module Check = struct

let process _ = ()
let untyped_value : Yojson.Safe.t = `List []
let _ = process(`List [untyped_value; untyped_value])

end
