module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("__proto__", `Assoc [("x", `Int 1)]);
    ("ordinary", `Int 2)
]

end
