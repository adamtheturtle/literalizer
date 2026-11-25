class Fixture_call_dotted_parameter_matches_root_Haxe_call {
    public static function main() {
        var outer = { inner: function(outer:Dynamic, n:Dynamic):Dynamic return null };
        outer.inner(1, 2);
    }
}
