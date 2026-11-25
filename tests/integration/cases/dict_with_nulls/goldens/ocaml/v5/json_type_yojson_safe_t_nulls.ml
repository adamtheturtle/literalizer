module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("name", `String "Alice");
    ("score", `Null);
    ("age", `Int 30)
]

end
