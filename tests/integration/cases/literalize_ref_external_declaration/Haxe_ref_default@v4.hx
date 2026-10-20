class Fixture_literalize_ref_external_declaration_Haxe_ref_default {
    public static function main() {
        function consume_widget(arg_value:Dynamic):Dynamic return null;
        final shared = ([
            1,
            2,
        ] : Array<Dynamic>);
        final my_data = shared;
        consume_widget(my_data);
    }
}
