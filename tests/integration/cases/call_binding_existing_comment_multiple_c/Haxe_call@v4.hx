class Fixture_call_binding_existing_comment_multiple_c_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = make_widget(42);
        make_widget(my_data);
        my_data = make_widget(my_data); // note
        // extra
        make_widget(my_data);
    }
}
