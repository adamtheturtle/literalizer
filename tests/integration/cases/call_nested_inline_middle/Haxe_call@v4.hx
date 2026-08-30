class Fixture_call_nested_inline_middle_Haxe_call {
    public static function main() {
        function f(ops:Dynamic):Dynamic return null;
        f(([(["DEL", "b", "10"] : Array<Dynamic>), (["ADD", "a", "x"] : Array<Dynamic>)] : Array<Dynamic>));  // note
    }
}
