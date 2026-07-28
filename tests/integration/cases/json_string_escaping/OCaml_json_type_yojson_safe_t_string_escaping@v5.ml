module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("$key", `String "a\"b\tcé #{world} $ident")
]

end
