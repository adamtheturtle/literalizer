class Fixture_dict_deeply_nested_singleton_sequences_Haxe {
    public static function main() {
        final my_data = ([
            "deep" => ([([([([1] : Array<Dynamic>)] : Array<Dynamic>)] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
