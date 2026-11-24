class Fixture_call_ref_bound_list_null_hint_Haxe_call {
    public static function main() {
        function consume(value:Dynamic):Dynamic return null;
        final item = ([
            1,
            2,
        ] : Array<Dynamic>);
        consume(item);
    }
}
