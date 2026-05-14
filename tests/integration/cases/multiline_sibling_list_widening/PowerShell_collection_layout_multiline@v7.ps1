$my_data = @{
    "omap_value" = [ordered]@{
        "first" = 1
    };
    "sibling_lists" = @{
        "numbers" = @(
            1;
            2
        );
        "strings" = @(
            "x";
            "y"
        )
    };
    "ref_marker_present" = @(
        "`$keep";
        "z"
    )
}
