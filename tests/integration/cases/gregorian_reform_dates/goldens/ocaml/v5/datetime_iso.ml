module Check = struct

type val_t =
  | OStr of string
  | ODate of (int * int * int)
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("ancient_date", ODate (1500, 3, 1));
    ("modern_date", ODate (2024, 1, 15));
    ("before_date", ODate (1582, 10, 4));
    ("gap_date", ODate (1582, 10, 10));
    ("transition_date", ODate (1582, 10, 15));
    ("after_date", ODate (1582, 10, 16));
    ("before_naive", OStr "1582-10-04T12:30:00.000001");
    ("gap_naive", OStr "1582-10-10T12:30:00.500000");
    ("transition_positive", OStr "1582-10-15T00:30:00+18:00");
    ("transition_negative", OStr "1582-10-15T23:30:00-18:00");
    ("after_positive", OStr "1582-10-16T00:30:00+18:00")
]

end
