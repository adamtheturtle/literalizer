class Fixture_call_nested_list_whole_argument_Haxe_call {
    public static function main() {
        function f(a:Dynamic):Dynamic return null;
        f(([([1, 2] : Array<Dynamic>), ([3] : Array<Dynamic>)] : Array<Dynamic>));
    }
}
