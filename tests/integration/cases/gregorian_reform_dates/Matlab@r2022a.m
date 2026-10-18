my_data = struct(
    'before_date', datetime(1582, 10, 4),
    'gap_date', datetime(1582, 10, 10),
    'transition_date', datetime(1582, 10, 15),
    'after_date', datetime(1582, 10, 16),
    'before_naive', datetime(1582, 10, 4, 12, 30, 0.000001),
    'gap_naive', datetime(1582, 10, 10, 12, 30, 0.5),
    'transition_positive', datetime(1582, 10, 15, 0, 30, 0),
    'transition_negative', datetime(1582, 10, 15, 23, 30, 0),
    'after_positive', datetime(1582, 10, 16, 0, 30, 0)
);
