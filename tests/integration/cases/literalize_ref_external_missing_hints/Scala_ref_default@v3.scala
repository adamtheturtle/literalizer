object Fixture_literalize_ref_external_missing_hints_Scala_ref_default {
def consume_widget(arg_value: Any = null): Any = null
val item = List[Int](
    1,
    2,
)
var my_data = List[Int](
    1,
    2,
)
consume_widget(arg_value = my_data)
my_data = item
consume_widget(arg_value = my_data)
}
