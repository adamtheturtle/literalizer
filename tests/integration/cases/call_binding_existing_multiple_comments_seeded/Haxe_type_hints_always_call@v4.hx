class Fixture_call_binding_existing_multiple_comments_seeded_Haxe_type_hints_always_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        function consume_widget(count:Dynamic):Dynamic return null;
        var my_data:Dynamic = make_widget(42);
        consume_widget(my_data);
        my_data = make_widget(my_data); // note
        // extra
        consume_widget(my_data);
    }
}
