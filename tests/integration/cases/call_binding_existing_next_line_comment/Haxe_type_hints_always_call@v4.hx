class Fixture_call_binding_existing_next_line_comment_Haxe_type_hints_always_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        function consume_widget(count:Dynamic):Dynamic return null;
        var my_data:Dynamic = make_widget(42);
        consume_widget(my_data);
        my_data = make_widget(42);
        // note
        consume_widget(my_data);
    }
}
