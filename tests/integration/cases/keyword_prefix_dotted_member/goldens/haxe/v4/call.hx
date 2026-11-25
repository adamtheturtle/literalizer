class Fixture_keyword_prefix_dotted_member_Haxe_call {
    public static function main() {
        var thing = { first_value: function(value:Dynamic):Dynamic return null };
        thing.first_value(1);
    }
}
