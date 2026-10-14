using System;
class Check {
static object? consume(object? value = null) => null;
    public static void Main() {
consume(-2147483649);
consume(2147483648);
    }
}
