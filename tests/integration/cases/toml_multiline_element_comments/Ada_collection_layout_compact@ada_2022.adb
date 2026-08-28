with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("first", AList'[AInt (1), AInt (2)]),
        AEntry ("second", AInt (3))  -- About the second key.
    ];
begin
    null;
end Main;
