with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AInt (1)),
        AEntry ("b", AInt (1099511627776))
    ];
begin
    null;
end Main;
