class Fixture_call_existing_ref_arg_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        final existing = 42;
        process(existing);
    }
}
