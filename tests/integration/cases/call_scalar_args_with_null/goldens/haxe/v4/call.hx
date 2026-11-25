class Fixture_call_scalar_args_with_null_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        process(null);
        process("hello");
    }
}
