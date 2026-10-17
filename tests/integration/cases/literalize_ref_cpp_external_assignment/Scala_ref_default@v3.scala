object Fixture_literalize_ref_cpp_external_assignment_Scala_ref_default {
def consume_widget(_arg: Any = null): Any = null
val ref_data = List[Int](
    1,
    2,
)
val my_data = List[Int](
    0,
)
consume_widget(_arg = my_data)
my_data = ref_data
consume_widget(_arg = my_data)
}
