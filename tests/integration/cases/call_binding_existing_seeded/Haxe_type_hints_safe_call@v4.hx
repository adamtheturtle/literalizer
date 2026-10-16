class Fixture_call_binding_existing_seeded_Haxe_type_hints_safe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data = make_widget(42);
        make_widget(my_data);
        my_data = make_widget(my_data);
        make_widget(my_data);
    }
}
