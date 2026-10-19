class Fixture_tuple_fields_with_nested_vectors_Haxe {
    public static function main() {
        final my_data = ([
            "lint" => ([2, ([] : Array<Dynamic>)] : Array<Dynamic>),
            "test" => ([5, (["compile"] : Array<Dynamic>)] : Array<Dynamic>),
            "package" => ([7, (["link", "test"] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
