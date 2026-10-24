module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("fffe", `String "￾");
    ("ffff", `String "￿")
]

end
