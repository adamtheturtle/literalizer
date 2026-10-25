with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- first dotted key
        -- second dotted key
        AEntry ("a", AMap'[AEntry ("b", AInt (1)), AEntry ("c", AInt (2))])
    ];
begin
    null;
end Main;
