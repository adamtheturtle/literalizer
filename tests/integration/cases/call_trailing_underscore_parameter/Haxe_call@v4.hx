class Fixture_call_trailing_underscore_parameter_Haxe_call {
    public static function main() {
        function do_thing(x_:Dynamic):Dynamic return null;
        do_thing(1);
        do_thing(2);
    }
}
