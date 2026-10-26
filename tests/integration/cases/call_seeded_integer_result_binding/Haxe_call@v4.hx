class Fixture_call_seeded_integer_result_binding_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        function consume(count:Dynamic):Dynamic return null;
        var my_data = make_widget(42);
        consume(my_data);
        my_data = make_widget(42);
        consume(my_data);
    }
}
