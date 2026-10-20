class Fixture_call_unused_bound_reference_Haxe_call {
    public static function main() {
        function f(value:Dynamic):Dynamic return null;
        f(([1, 2] : Array<Dynamic>));
    }
}
