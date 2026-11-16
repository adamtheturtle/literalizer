class Fixture_literalize_ref_external_scalar_assignment_Haxe_ref_default {
    public static function main() {
        function consume_widget(arg_value:Dynamic):Dynamic return null;
        var my_data = 0;
        final shared = 1;
        consume_widget(my_data);
        my_data = shared;
        consume_widget(my_data);
    }
}
