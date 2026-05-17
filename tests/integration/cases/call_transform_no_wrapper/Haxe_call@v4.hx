class Fixture_call_transform_no_wrapper_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        process("hello");
        process(42);
        process(true);
    }
}
