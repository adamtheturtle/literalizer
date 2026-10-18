with A_Stub; use A_Stub;
procedure Main is
    sibling_map : A_Val := AMap'[
        AEntry ("k", AInt (2))
    ];
    my_data : A_Val := AList'[
        AMap'[AEntry ("k", AInt (1))],
        sibling_map
    ];
begin
    null;
end Main;
