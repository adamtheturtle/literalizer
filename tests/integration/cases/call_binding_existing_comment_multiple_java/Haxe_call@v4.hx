class Fixture_call_binding_existing_comment_multiple_java_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = make_widget(null);
        my_data = make_widget(42); // note
        // extra
    }
}
