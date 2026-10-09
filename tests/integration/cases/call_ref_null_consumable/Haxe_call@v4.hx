class Fixture_call_ref_null_consumable_Haxe_call {
    public static function main() {
        function consume(value:Dynamic):Dynamic return null;
        final my_null = null;
        final regular_null = null;
        consume(my_null);
        consume(regular_null);
    }
}
