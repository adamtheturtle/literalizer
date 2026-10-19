with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[AEntry ("k", AInt (1))]),
        AEntry ("b", AMap'[AEntry ("k", AStr ("s"))])
    ];
begin
    null;
end Main;
