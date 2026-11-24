class Fixture_call_ignored_parameter_collision_Haxe_call {
    public static function main() {
        function f(x:Dynamic, _x:Dynamic):Dynamic return null;
        f(1, 2);
    }
}
