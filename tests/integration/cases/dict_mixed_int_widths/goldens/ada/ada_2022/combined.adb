with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AInt (1)),
        AEntry ("b", AInt (3000000000)),
        AEntry ("c", AStr ("x"))
    ];
begin
    my_data := AMap'[
        AEntry ("a", AInt (1)),
        AEntry ("b", AInt (3000000000)),
        AEntry ("c", AStr ("x"))
    ];
end Main;
