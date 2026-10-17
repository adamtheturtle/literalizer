class Fixture_literalize_ref_zig_external_native_assignment_Haxe_ref_default {
    public static function main() {
        function consume_widget(_arg:Dynamic):Dynamic return null;
        final shared = ([
            1,
            2,
        ] : Array<Dynamic>);
        var my_data = ([
            0,
        ] : Array<Dynamic>);
        consume_widget(my_data);
        my_data = shared;
        consume_widget(my_data);
    }
}
