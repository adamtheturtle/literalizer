object Fixture_literalize_ref_native_empty_array_both_Scala_ref {
var shared = List[Int]()
var second = List[Int](
    1,
    2,
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
