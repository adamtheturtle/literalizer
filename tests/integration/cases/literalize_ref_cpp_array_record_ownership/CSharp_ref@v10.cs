record Record1(int[] Values);
record Record2(int[][] Nested);
record Record0(Record1 Trivial, Record2 Nested);
class Check {
    public static void Main() {
var Trivial = new Record1(
    new int[] {
        1,
        2
    }
);
var Nested = new Record2(
    new int[][] {
        new int[] {
            1,
            2
        },
        new int[] {
            3,
            4
        }
    }
);
var my_data = new Record0(
    Trivial,
    Nested
);
    }
}
