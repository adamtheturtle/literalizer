my_data = struct(
    'ancient_date', "1500-03-01",
    'modern_date', "2024-01-15",
    'before_date', "1582-10-04",
    'gap_date', "1582-10-10",
    'transition_date', "1582-10-15",
    'after_date', "1582-10-16",
    'before_naive', datetime(1582, 10, 4, 12, 30, 0.000001),
    'gap_naive', datetime(1582, 10, 10, 12, 30, 0.5),
    'transition_positive', datetime(1582, 10, 15, 0, 30, 0),
    'transition_negative', datetime(1582, 10, 15, 23, 30, 0),
    'after_positive', datetime(1582, 10, 16, 0, 30, 0)
);
