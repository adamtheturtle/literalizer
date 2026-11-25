class Fixture_call_nullable_object_conditional_per_element_Haxe_type_hints_always_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        final my_data:Dynamic = make_widget(7) != null ?
        make_widget(7) // inner
        : null; // trailing
    }
}
