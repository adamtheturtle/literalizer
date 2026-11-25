object Fixture_call_seeded_nullable_result_binding_Scala_call {
def make_widget(count: Any = null): Any = null
def consume(count: Any = null): Any = null
var my_data = make_widget(count = null)
consume(count = my_data)
my_data = make_widget(count = 42)
consume(count = my_data)
}
