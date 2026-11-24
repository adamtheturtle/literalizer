class Fixture_call_whole_list_argument_Haxe_type_hints_always_call {
    public static function main() {
        function f(a:Dynamic):Dynamic return null;
        f(([1] : Array<Dynamic>));
    }
}
