class Fixture_call_existing_binding_seed_and_result_Haxe_call {
    public static function main() {
        function make_widget(count:Dynamic):Dynamic return null;
        function consume_widget(count:Dynamic):Dynamic return null;
        var my_data = make_widget(0);
        consume_widget(my_data);
        my_data = make_widget(1);
        consume_widget(my_data);
    }
}
