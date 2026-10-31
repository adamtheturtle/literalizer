using System;
record Record0(int A);
class Check {
static object? consume(object? stamp = null, object? value = null) => null;
    public static void Main() {
var item = new Record0(
    1
);
var stamp = new DateOnly(2001, 2, 3);
consume(stamp, item);
    }
}
