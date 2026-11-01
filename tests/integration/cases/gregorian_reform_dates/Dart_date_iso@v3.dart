final my_data = <String, dynamic>{
    "ancient_date": "1500-03-01",
    "modern_date": "2024-01-15",
    "before_date": "1582-10-04",
    "gap_date": "1582-10-10",
    "transition_date": "1582-10-15",
    "after_date": "1582-10-16",
    "before_naive": DateTime.utc(1582, 10, 4, 12, 30, 0, 0, 1),
    "gap_naive": DateTime.utc(1582, 10, 10, 12, 30, 0, 500, 0),
    "transition_positive": DateTime.parse("1582-10-15T00:30:00+18:00"),
    "transition_negative": DateTime.parse("1582-10-15T23:30:00-18:00"),
    "after_positive": DateTime.parse("1582-10-16T00:30:00+18:00"),
};
