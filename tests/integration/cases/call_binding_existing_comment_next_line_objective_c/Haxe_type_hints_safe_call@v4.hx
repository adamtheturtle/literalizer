class Fixture_call_binding_existing_comment_next_line_objective_c_Haxe_type_hints_safe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = make_widget(42);
        my_data = make_widget(my_data);
        // note
        make_widget(my_data);
    }
}
