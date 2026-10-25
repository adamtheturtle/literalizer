class Fixture_inconsistent_string_dict_shapes_in_seq_Haxe_combined {
    public static function main() {
        var my_data = ([
            (["first" => "Alice", "last" => "Smith"] : Map<String, Dynamic>),
            (["first" => "Bob", "middle" => "Quincy"] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
        my_data = ([
            (["first" => "Alice", "last" => "Smith"] : Map<String, Dynamic>),
            (["first" => "Bob", "middle" => "Quincy"] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
