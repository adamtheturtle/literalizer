class Fixture_call_binding_existing_inline_comment_seeded_Haxe_type_hints_safe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        function consume_widget(count:Dynamic):Dynamic return null;
        var my_data = make_widget(42);
        consume_widget(my_data);
        my_data = make_widget(my_data); // note
        consume_widget(my_data);
    }
}
