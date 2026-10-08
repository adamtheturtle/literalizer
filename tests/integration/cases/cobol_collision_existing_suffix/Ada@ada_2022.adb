with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a-b", AInt (1)),
        AEntry ("a-b-2", AInt (2)),
        AEntry ("a b", AInt (3))
    ];
begin
    null;
end Main;
