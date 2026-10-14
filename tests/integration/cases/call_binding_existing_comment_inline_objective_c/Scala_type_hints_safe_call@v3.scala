object Fixture_call_binding_existing_comment_inline_objective_c_Scala_type_hints_safe_call {
def make_widget(count: Any = null): Any = null
var my_data = make_widget(count = 42)
my_data = make_widget(count = my_data) // note
make_widget(count = my_data)
}
