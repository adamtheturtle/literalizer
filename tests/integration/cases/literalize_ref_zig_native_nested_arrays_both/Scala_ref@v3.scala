object Fixture_literalize_ref_zig_native_nested_arrays_both_Scala_ref {
var shared = List[Int](
    1,
    2,
)
var second = List[Int](
    3,
    4,
)
var my_data = List[List[Int]](
    shared,
    second,
)
my_data = List[List[Int]](
    shared,
    second,
)
}
