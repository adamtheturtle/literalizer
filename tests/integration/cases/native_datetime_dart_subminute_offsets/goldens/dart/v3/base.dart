final my_data = <String, List<DateTime>>{
    "stamps": <DateTime>[DateTime.utc(2001, 2, 3, 4, 5, 6, 123, 456).subtract(Duration(microseconds: 1000000)), DateTime.utc(2001, 2, 3, 4, 5, 6, 123, 456).subtract(Duration(microseconds: -1000000)), DateTime.utc(2001, 2, 3, 4, 5, 6, 123, 456).subtract(Duration(microseconds: 1)), DateTime.utc(2001, 2, 3, 4, 5, 6, 123, 456).subtract(Duration(microseconds: -1)), DateTime.utc(2001, 2, 3, 4, 5, 6, 123, 456).subtract(Duration(microseconds: 19815000001)), DateTime.utc(2001, 2, 3, 4, 5, 6, 123, 456).subtract(Duration(microseconds: -19815000001))],
};
