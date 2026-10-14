record Record0(bool[] Flags, double[] Values, int[] Ints, string[] Text, bool[][] NestedFlags, double[][] NestedValues);
class Check {
    public static void Main() {
var my_data = new Record0(
    new bool[] {
        true,
        false
    },
    new double[] {
        1.5,
        -2.25
    },
    new int[] {
        1,
        2
    },
    new string[] {
        "a"
    },
    new bool[][] {
        new bool[] {
            true
        },
        new bool[] {
            false
        }
    },
    new double[][] {
        new double[] {
            1.5
        },
        new double[] {
            2.25
        }
    }
);
    _ = my_data;
    }
}
