final my_data = <String, List<DateTime>>{
    "stamps": <DateTime>[DateTime.utc(1, 1, 1, 0, 0, 0).subtract(Duration(microseconds: 1)), DateTime.utc(9999, 12, 31, 23, 59, 59, 999, 999).subtract(Duration(microseconds: -1))],
};
