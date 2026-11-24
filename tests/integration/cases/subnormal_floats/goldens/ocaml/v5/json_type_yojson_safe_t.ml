module Check = struct

let my_data : Yojson.Safe.t = `List [
    `Float 5.0e-324;
    `Float (-5.0e-324);
    `Float 1.0e-310
]

end
