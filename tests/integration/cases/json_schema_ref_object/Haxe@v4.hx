class Fixture_json_schema_ref_object_Haxe {
    public static function main() {
        final my_data = ([
            "schema" => (["$ref" => "#/defs/Foo"] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
