module Check = struct

let shared : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let build : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let json_object : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let json_allocator : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let json_entries : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let json_entry : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let my_data : Yojson.Safe.t = `Assoc [
    ("field", shared);
    ("nested", `List [shared; `Assoc []]);
    ("build", build);
    ("json_object", json_object);
    ("json_allocator", json_allocator);
    ("json_entries", json_entries);
    ("json_entry", json_entry)
]

end
