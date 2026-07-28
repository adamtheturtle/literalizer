class Fixture_call_unknown_ref_nested_Haxe_call {
    public static function main() {
        function process(known_value:Dynamic, nested_missing:Dynamic):Dynamic return null;
        final known_value = true;
        final unknown_value = true;
        process(known_value, unknown_value);
    }
}
