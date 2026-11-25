module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("ancient_date", `String "1500-03-01");
    ("modern_date", `String "2024-01-15");
    ("before_date", `String "1582-10-04");
    ("gap_date", `String "1582-10-10");
    ("transition_date", `String "1582-10-15");
    ("after_date", `String "1582-10-16");
    ("before_naive", `String "1582-10-04T12:30:00.000001");
    ("gap_naive", `String "1582-10-10T12:30:00.500000");
    ("transition_positive", `String "1582-10-15T00:30:00+18:00");
    ("transition_negative", `String "1582-10-15T23:30:00-18:00");
    ("after_positive", `String "1582-10-16T00:30:00+18:00")
]

end
