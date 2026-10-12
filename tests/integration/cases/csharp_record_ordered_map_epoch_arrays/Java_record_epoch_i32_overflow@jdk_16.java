import java.util.Map;
record Record0(java.util.ArrayList values, boolean flag, long[][] direct_arrays) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("wide", new long[][]{
            new long[]{
                2208988800L
            },
            new long[]{}
        }),
        Map.entry("narrow", new long[][]{
            new long[]{
                946684800
            }
        }),
        Map.entry("negative", new long[][]{
            new long[]{
                -2208988800L
            }
        }),
        Map.entry("shifted", new long[][]{
            new long[]{
                2208988800L
            }
        }),
        Map.entry("mixed_width", new long[][]{
            new long[]{
                946684800
            },
            new long[]{
                2208988800L
            }
        }),
        Map.entry("text", "preserve")
    )),
    true,
    new long[][]{
        new long[]{
            2208988800L
        },
        new long[]{}
    }
);
    }
}
