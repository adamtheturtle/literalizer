class Fixture_call_reserved_target_member_casefold_Haxe_call {
    public static function main() {
        var obj = { BEGIN: function(a:Dynamic):Dynamic return null };
        obj.BEGIN(42);
    }
}
