class Fixture_call_binding_existing_comment_multiple_objective_c_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = 42;
        my_data = make_widget(my_data); // note
        // extra
        make_widget(my_data);
    }
}
