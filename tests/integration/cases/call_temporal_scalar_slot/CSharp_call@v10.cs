using System;
class Check {
static object process(object value = null) => null;
    public static void Main() {
process(new TimeOnly(9, 30, 0));
process(new DateTime(2024, 1, 15, 0, 0, 0));
process(1);
    }
}
