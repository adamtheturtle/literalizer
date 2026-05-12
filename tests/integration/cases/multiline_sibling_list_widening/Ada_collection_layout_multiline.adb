with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("omap_value", AMap'[
            AEntry ("first", AInt (1))
        ]),
        AEntry ("sibling_lists", AMap'[
            AEntry ("numbers", AList'[
                AInt (1),
                AInt (2)
            ]),
            AEntry ("strings", AList'[
                AStr ("x"),
                AStr ("y")
            ])
        ]),
        AEntry ("ref_marker_present", AList'[
            AStr ("$keep"),
            AStr ("z")
        ])
    ];
begin
    null;
end Main;
