record Record1(int X, object Y);
record Record2(object X, object Y);
record Record3(int X, int Y);
record Record0(Record1 Nullable, Record2 NullFields, Record3 Plain);
class Check {
    public static void Main() {
var Nullable = new Record1(
    1,
    (object?)null
);
var NullFields = new Record2(
    (object?)null,
    (object?)null
);
var Plain = new Record3(
    1,
    2
);
var my_data = new Record0(
    Nullable,
    NullFields,
    Plain
);
    }
}
