record Record0(int[] Pair, object[] Mixed, object[] Triple, object[] Nested, object[] Empty, int[] Single, int[] Long);
class Check {
    public static void Main() {
var my_data = new Record0(
    new int[] {
        1,
        2
    },
    new object[] {
        1,
        "text"
    },
    new object[] {
        1,
        "text",
        true
    },
    new object[] {
        new object[] {
            1,
            "text"
        },
        new object[] {
            2,
            false,
            3.5
        }
    },
    new object[] {},
    new int[] {
        1
    },
    new int[] {
        1,
        2,
        3,
        4
    }
);
    }
}
