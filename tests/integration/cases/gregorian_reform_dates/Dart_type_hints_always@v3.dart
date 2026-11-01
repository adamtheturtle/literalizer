final Map<String, dynamic> my_data = <String, dynamic>{
    "ancient_date": DateTime.utc(1500, 3, 1),
    "modern_date": DateTime.utc(2024, 1, 15),
    "before_date": DateTime.utc(1582, 10, 4),
    "gap_date": DateTime.utc(1582, 10, 10),
    "transition_date": DateTime.utc(1582, 10, 15),
    "after_date": DateTime.utc(1582, 10, 16),
    "before_naive": DateTime.utc(1582, 10, 4, 12, 30, 0, 0, 1),
    "gap_naive": DateTime.utc(1582, 10, 10, 12, 30, 0, 500, 0),
    "transition_positive": DateTime.parse("1582-10-15T00:30:00+18:00"),
    "transition_negative": DateTime.parse("1582-10-15T23:30:00-18:00"),
    "after_positive": DateTime.parse("1582-10-16T00:30:00+18:00"),
};
