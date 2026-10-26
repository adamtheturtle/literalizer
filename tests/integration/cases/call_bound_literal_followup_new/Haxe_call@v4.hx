class Fixture_call_bound_literal_followup_new_Haxe_call {
    public static function main() {
        function make_widget(value:Dynamic):Dynamic return null;
        function consume(value:Dynamic):Dynamic return null;
        final my_data = make_widget(42);
        consume(my_data);
    }
}
