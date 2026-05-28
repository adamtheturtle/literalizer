module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("name", `String "Alice");
    ("age", `Int 30);
    ("active", `Bool true)
]

end
