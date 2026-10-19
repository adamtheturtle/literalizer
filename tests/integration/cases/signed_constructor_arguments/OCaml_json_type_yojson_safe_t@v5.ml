module Check = struct

let my_data : Yojson.Safe.t = `List [
    `Int (-42);
    `Int 0;
    `Int 42;
    `Float (-1.25);
    `Float 0.0;
    `Float 1.25
]

end
