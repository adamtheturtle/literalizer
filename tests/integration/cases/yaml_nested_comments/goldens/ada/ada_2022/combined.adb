with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[
            -- inner note
            AEntry ("b", AInt (1))  -- inline b
        ]),
        AEntry ("list", AList'[
            AInt (1),  -- first
            AInt (2)  -- second
        ])
    ];
begin
    my_data := AMap'[
        AEntry ("a", AMap'[
            -- inner note
            AEntry ("b", AInt (1))  -- inline b
        ]),
        AEntry ("list", AList'[
            AInt (1),  -- first
            AInt (2)  -- second
        ])
    ];
end Main;
