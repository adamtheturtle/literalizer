class Fixture_call_null_and_array_arguments_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        process(null);
        process(([1, 2] : Array<Dynamic>));
    }
}
