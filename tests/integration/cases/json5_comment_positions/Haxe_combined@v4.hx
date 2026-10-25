class Fixture_json5_comment_positions_Haxe_combined {
    public static function main() {
        var my_data = ([
            //
            // document heading
            // before the first entry
            // after the key
            // before the value
            "counts" => ([
                // before the first item
                1,  // inline block after the comma
                // before the second item
                2,
                // trailing inside the array
            ] : Array<Dynamic>),  // after the nested collection
            "more" => ([
                3,
                //
                // block heading
                // block continuation
                4,  // final inline
            ] : Array<Dynamic>),
            // trailing inside the object
            // after the root
            // after the document
        ] : Map<String, Dynamic>);
        my_data = ([
            //
            // document heading
            // before the first entry
            // after the key
            // before the value
            "counts" => ([
                // before the first item
                1,  // inline block after the comma
                // before the second item
                2,
                // trailing inside the array
            ] : Array<Dynamic>),  // after the nested collection
            "more" => ([
                3,
                //
                // block heading
                // block continuation
                4,  // final inline
            ] : Array<Dynamic>),
            // trailing inside the object
            // after the root
            // after the document
        ] : Map<String, Dynamic>);
    }
}
