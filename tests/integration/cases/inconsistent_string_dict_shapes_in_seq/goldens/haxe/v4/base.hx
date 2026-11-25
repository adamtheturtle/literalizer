class Fixture_inconsistent_string_dict_shapes_in_seq_Haxe {
    public static function main() {
        final my_data = ([
            (["first" => "Alice", "last" => "Smith"] : Map<String, Dynamic>),
            (["first" => "Bob", "middle" => "Quincy"] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
