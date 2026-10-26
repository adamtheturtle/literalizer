object Fixture_call_bound_literal_followup_existing_Scala_call {
def make_widget(value: Any = null): Any = null
def consume(value: Any = null): Any = null
var my_data = make_widget(value = 42)
consume(value = my_data)
my_data = make_widget(value = 42)
consume(value = my_data)
}
