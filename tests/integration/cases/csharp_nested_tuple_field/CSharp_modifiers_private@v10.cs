using System;
class Check {
private (ValueTuple, ValueTuple<int>, (int, int), (int, string, bool, object), (int, int, int, int, int, int, int, int)) my_data = (
    ValueTuple.Create(),
    ValueTuple.Create(1),
    (1, 2),
    (1, "x", true, (object?)null),
    (1, 2, 3, 4, 5, 6, 7, 8)
);
    public static void Main() {}
}
