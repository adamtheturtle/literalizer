class Fixture_call_binding_existing_comment_next_line_c_Haxe_type_hints_always_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data:Dynamic = make_widget(42);
        make_widget(my_data);
        my_data = make_widget(my_data);
        // note
        make_widget(my_data);
    }
}
