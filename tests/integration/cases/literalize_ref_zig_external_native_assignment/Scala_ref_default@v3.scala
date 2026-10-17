object Fixture_literalize_ref_zig_external_native_assignment_Scala_ref_default {
def consume_widget(_arg: Any = null): Any = null
val shared = List[Int](
    1,
    2,
)
var my_data = List[Int](
    0,
)
consume_widget(_arg = my_data)
my_data = shared
consume_widget(_arg = my_data)
}
