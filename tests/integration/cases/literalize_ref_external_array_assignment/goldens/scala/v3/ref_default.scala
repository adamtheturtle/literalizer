object Fixture_literalize_ref_external_array_assignment_Scala_ref_default {
def consume_widget(arg_value: Any = null): Any = null
val shared = List[Int](
    1,
    2,
)
var my_data = List[Int](
    0,
)
consume_widget(arg_value = my_data)
my_data = shared
consume_widget(arg_value = my_data)
}
