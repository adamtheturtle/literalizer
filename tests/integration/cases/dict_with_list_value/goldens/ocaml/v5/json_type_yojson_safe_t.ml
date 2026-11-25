module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("name", `String "Alice");
    ("scores", `List [`Int 10; `Int 20; `Int 30])
]

end
