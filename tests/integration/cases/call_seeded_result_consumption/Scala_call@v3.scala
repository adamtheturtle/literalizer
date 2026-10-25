object Fixture_call_seeded_result_consumption_Scala_call {
def make_widget(count: Any = null): Any = null
def consume_widget(count: Any = null): Any = null
var my_data = make_widget(count = 0)
consume_widget(count = my_data)
my_data = make_widget(count = 1)
consume_widget(count = my_data)
}
