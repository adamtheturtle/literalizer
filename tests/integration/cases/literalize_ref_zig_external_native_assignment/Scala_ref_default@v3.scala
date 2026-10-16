object Fixture_literalize_ref_zig_external_native_assignment_Scala_ref_default {
val shared = List[Int](
    1,
    2,
)
var my_data = List[Int](
    0,
)
_ = &my_data;
my_data = shared
_ = &my_data;
}
