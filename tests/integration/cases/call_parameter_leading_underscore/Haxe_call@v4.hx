class Fixture_call_parameter_leading_underscore_Haxe_call {
    public static function main() {
        function f(_x:Dynamic):Dynamic return null;
        f(1);
    }
}
