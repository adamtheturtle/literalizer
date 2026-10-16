class Fixture_call_existing_binding_ada_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = make_widget(0);
        make_widget(my_data);
        my_data = make_widget(1);
        make_widget(my_data);
    }
}
