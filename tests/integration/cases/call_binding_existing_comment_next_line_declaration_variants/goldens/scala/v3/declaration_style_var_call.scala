object Fixture_call_binding_existing_comment_next_line_declaration_variants_Scala_declaration_style_var_call {
def make_widget(count: Any = null): Any = null
def consume(count: Any = null): Any = null
var my_data = make_widget(count = 42)
consume(count = my_data)
my_data = make_widget(count = 42)
// note
consume(count = my_data)
}
