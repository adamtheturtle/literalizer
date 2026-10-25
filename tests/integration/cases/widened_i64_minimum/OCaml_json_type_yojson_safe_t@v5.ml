module Check = struct

let my_data : Yojson.Safe.t = `List [
    `Intlit "-9223372036854775808";
    `Int 5
]

end
