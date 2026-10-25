class Fixture_literalize_ref_external_unrelated_hints_Haxe_ref_default {
    public static function main() {
        function consume_widget(arg_value:Dynamic):Dynamic return null;
        final missing = ([
            1,
            2,
        ] : Array<Dynamic>);
        final my_data = missing;
        consume_widget(my_data);
    }
}
