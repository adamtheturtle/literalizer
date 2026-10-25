class Fixture_literalize_ref_external_assignment_Haxe_ref_default {
    public static function main() {
        function consume_widget(arg_value:Dynamic):Dynamic return null;
        final ref_data = ([
            1,
            2,
        ] : Array<Dynamic>);
        var my_data = ([
            0,
        ] : Array<Dynamic>);
        consume_widget(my_data);
        my_data = ref_data;
        consume_widget(my_data);
    }
}
