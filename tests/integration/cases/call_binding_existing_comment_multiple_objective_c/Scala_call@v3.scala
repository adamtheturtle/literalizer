object Fixture_call_binding_existing_comment_multiple_objective_c_Scala_call {
def make_widget(count: Any = null): Any = null
var my_data = make_widget(count = 42)
my_data = make_widget(count = my_data) // note
// extra
make_widget(count = my_data)
}
