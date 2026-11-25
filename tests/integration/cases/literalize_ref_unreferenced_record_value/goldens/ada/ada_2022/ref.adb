with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("main", AMap'[AEntry ("x", AInt (1)), AEntry ("y", AStr ("s"))])
    ];
begin
    null;
end Main;
