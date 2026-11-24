module Check = struct

let my_data : Yojson.Safe.t = `List [
    `List [`Int 1; `String "a"];
    `List [`Int 2; `String "b"]
]

end
