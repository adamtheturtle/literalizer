record Record1(int item) {}
record Record2(Object item) {}
record Record0(Object[] integers, Object[] nulls, Object[] nested, Object[] reversed) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new Object[]{
        new Record1[]{},
        new Record1[]{
            new Record1(
                1
            )
        }
    },
    new Object[]{
        new Record2[]{},
        new Record2[]{
            new Record2(
                null
            )
        }
    },
    new Object[]{
        new Object[]{
            new Record1[]{},
            new Record1[]{
                new Record1(
                    2
                )
            }
        },
        new Object[]{
            new Record1[]{
                new Record1(
                    3
                )
            },
            new Record1[]{}
        }
    },
    new Object[]{
        new Record1[]{
            new Record1(
                4
            )
        },
        new Record1[]{}
    }
);
my_data = new Record0(
    new Object[]{
        new Record1[]{},
        new Record1[]{
            new Record1(
                1
            )
        }
    },
    new Object[]{
        new Record2[]{},
        new Record2[]{
            new Record2(
                null
            )
        }
    },
    new Object[]{
        new Object[]{
            new Record1[]{},
            new Record1[]{
                new Record1(
                    2
                )
            }
        },
        new Object[]{
            new Record1[]{
                new Record1(
                    3
                )
            },
            new Record1[]{}
        }
    },
    new Object[]{
        new Record1[]{
            new Record1(
                4
            )
        },
        new Record1[]{}
    }
);
    }
}
