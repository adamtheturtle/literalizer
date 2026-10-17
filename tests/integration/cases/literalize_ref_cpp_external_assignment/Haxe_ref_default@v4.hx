class Fixture_literalize_ref_cpp_external_assignment_Haxe_ref_default {
    public static function main() {
        function consume_widget(_arg:Dynamic):Dynamic return null;
        final ref_data = ([
            1,
            2,
        ] : Array<Dynamic>);
        final my_data = ([
            0,
        ] : Array<Dynamic>);
        consume_widget(my_data);
        my_data = ref_data;
        consume_widget(my_data);
    }
}
