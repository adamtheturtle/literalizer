record Record1(int Item);
record Record2(object? Item);
record Record0(Record1[][] Integers, Record2[][] Nulls, Record1[][][] Nested, Record1[][] Reversed);
class Check {
    public static void Main() {
var my_data = new Record0(
    new[] {
        new Record1[] {},
        new[] {
            new Record1(
                1
            )
        }
    },
    new[] {
        new Record2[] {},
        new[] {
            new Record2(
                (object?)null
            )
        }
    },
    new[] {
        new[] {
            new Record1[] {},
            new[] {
                new Record1(
                    2
                )
            }
        },
        new[] {
            new[] {
                new Record1(
                    3
                )
            },
            new Record1[] {}
        }
    },
    new[] {
        new[] {
            new Record1(
                4
            )
        },
        new Record1[] {}
    }
);
    _ = my_data;
    }
}
