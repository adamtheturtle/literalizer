class Fixture_call_case_distinct_dotted_parts_Haxe_call_value_result {
    public static function main() {
        var a = { foo: { Foo: { bar: function(x:Dynamic):Dynamic return null } } };
        final my_data = a.foo.Foo.bar(([1] : Array<Dynamic>));
    }
}
