class Fixture_literalize_ref_external_missing_hints_Haxe_ref_default {
    public static function main() {
        function consume_widget(arg_value:Dynamic):Dynamic return null;
        final item = ([
            1,
            2,
        ] : Array<Dynamic>);
        var my_data = ([
            1,
            2,
        ] : Array<Dynamic>);
        consume_widget(my_data);
        my_data = item;
        consume_widget(my_data);
    }
}
