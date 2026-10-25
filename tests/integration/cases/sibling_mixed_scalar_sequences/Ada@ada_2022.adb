with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("left", AList'[AInt (1), AStr ("one")]),
        AEntry ("right", AList'[AInt (2), AStr ("two")])
    ];
begin
    null;
end Main;
