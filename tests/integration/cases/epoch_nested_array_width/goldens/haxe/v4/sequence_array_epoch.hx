class Fixture_epoch_nested_array_width_Haxe_sequence_array_epoch {
    public static function main() {
        final my_data = ([
            "positive" => ([(["item" => ([2147483648] : Array<Dynamic>)] : Map<String, Dynamic>)] : Array<Dynamic>),
            "negative" => ([(["item" => ([-2147483649] : Array<Dynamic>)] : Map<String, Dynamic>)] : Array<Dynamic>),
            "mixed" => ([(["item" => ([0, 2147483648] : Array<Dynamic>)] : Map<String, Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
