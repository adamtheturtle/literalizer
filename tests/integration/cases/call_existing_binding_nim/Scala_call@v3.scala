object Fixture_call_existing_binding_nim_Scala_call {
def make_widget(count: Any = null): Any = null
var my_data = make_widget(count = 0)
my_data = make_widget(count = 1)
make_widget(count = my_data)
}
