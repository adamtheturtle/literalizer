with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("flow", AList'[
            AInt (1),
            -- After the first element.
            AInt (2)
        ]),
        -- Between the key and its value.
        AEntry ("gap", AInt (3)),
        -- On the block scalar header.
        AEntry ("block", AStr ("Text." & Character'Val(10))),
        AEntry ("nested", AList'[
            AInt (1),
            AInt (1)
            -- On the nested alias.
        ]),
        AEntry ("anchored", AInt (4)),
        AEntry ("alias", AInt (4))
        -- On the alias.
    ];
begin
    my_data := AMap'[
        AEntry ("flow", AList'[
            AInt (1),
            -- After the first element.
            AInt (2)
        ]),
        -- Between the key and its value.
        AEntry ("gap", AInt (3)),
        -- On the block scalar header.
        AEntry ("block", AStr ("Text." & Character'Val(10))),
        AEntry ("nested", AList'[
            AInt (1),
            AInt (1)
            -- On the nested alias.
        ]),
        AEntry ("anchored", AInt (4)),
        AEntry ("alias", AInt (4))
        -- On the alias.
    ];
end Main;
