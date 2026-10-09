using System;
class Check {
static object process(object value = null, object extra = null) => null;
    public static void Main() {
process(1, "hello");
process("two", false);
process(3.5, (object?)null);
    }
}
