record Record0(boolean[] flags, double[] values, int[] ints, String[] text, boolean[][] nested_flags, double[][] nested_values) {}
class Main {
    public static void main() {
Record0 my_data = new Record0(
    new boolean[]{
        true,
        false
    },
    new double[]{
        1.5,
        -2.25
    },
    new int[]{
        1,
        2
    },
    new String[]{
        "a"
    },
    new boolean[][]{
        new boolean[]{
            true
        },
        new boolean[]{
            false
        }
    },
    new double[][]{
        new double[]{
            1.5
        },
        new double[]{
            2.25
        }
    }
);
    }
}
