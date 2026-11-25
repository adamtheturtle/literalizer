class Fixture_call_binding_existing_comment_multiple_nullable_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        function consume(count:Dynamic):Dynamic return null;
        var my_data = make_widget(null);
        consume(my_data);
        my_data = make_widget(42); // note
        // extra
        consume(my_data);
    }
}
