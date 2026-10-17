class Fixture_literalize_ref_cpp_external_missing_Haxe_ref_default {
    public static function main() {
        function consume_widget(_arg:Dynamic):Dynamic return null;
        final item = ([
            1,
            2,
        ] : Array<Dynamic>);
        final my_data = ([
            1,
            2,
        ] : Array<Dynamic>);
        consume_widget(my_data);
        my_data = item;
        consume_widget(my_data);
    }
}
