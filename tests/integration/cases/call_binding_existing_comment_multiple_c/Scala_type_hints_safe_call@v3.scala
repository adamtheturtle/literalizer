object Fixture_call_binding_existing_comment_multiple_c_Scala_type_hints_safe_call {
def make_widget(count: Any = null): Any = null
val my_data = 42
my_data = make_widget(count = my_data) // note
// extra
make_widget(count = my_data)
}
