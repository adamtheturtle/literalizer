with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AList'[AInt (1), AInt (2), AInt (3)]),  -- inline a
        AEntry ("b", AInt (2))  -- inline b
    ];
begin
    null;
end Main;
