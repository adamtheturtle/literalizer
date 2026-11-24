class Fixture_nested_list_of_dicts_Haxe {
    public static function main() {
        final my_data = ([
            ([(["name" => "Alice"] : Map<String, Dynamic>), (["name" => "Bob"] : Map<String, Dynamic>)] : Array<Dynamic>),
            ([(["name" => "Charlie"] : Map<String, Dynamic>), (["name" => "Dave"] : Map<String, Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
