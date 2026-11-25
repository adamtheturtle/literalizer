with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("numbers", AList'[AInt (1), AInt (2)]),
        AEntry ("nested", AMap'[AEntry ("inner", AList'[AInt (3)])]),
        AEntry ("mixed", AList'[AInt (4), AStr ("five")])
    ];
begin
    null;
end Main;
