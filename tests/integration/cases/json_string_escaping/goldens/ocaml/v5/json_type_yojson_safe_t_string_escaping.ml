module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("$key", `String "a\"b\tcé #{world} $ident");
    ("trailing multi-byte", `String "café")
]

end
