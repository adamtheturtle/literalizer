class Fixture_call_ref_nested_converted_Haxe_call {
    public static function main() {
        function process(data:Dynamic):Dynamic return null;
        final myVar = 42;
        process(([myVar, 42, "static"] : Array<Dynamic>));
    }
}
