class Fixture_literalize_ref_unresolved_unrelated_values_Haxe_ref_default {
    public static function main() {
        function consume_widget(arg_value:Dynamic):Dynamic return null;
        final a = 0;
        final my_data = ([
            a,
            1,
        ] : Array<Dynamic>);
        consume_widget(my_data);
    }
}
