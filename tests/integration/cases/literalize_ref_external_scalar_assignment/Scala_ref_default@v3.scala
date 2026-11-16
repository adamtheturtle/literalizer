object Fixture_literalize_ref_external_scalar_assignment_Scala_ref_default {
def consume_widget(arg_value: Any = null): Any = null
var my_data = 0
val shared = 1
consume_widget(arg_value = my_data)
my_data = shared
consume_widget(arg_value = my_data)
}
