with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("__proto__", AMap'[AEntry ("x", AInt (1))]),
        AEntry ("n", AMap'[AEntry ("__proto__", AInt (3))]),
        AEntry ("y", AInt (2))
    ];
begin
    null;
end Main;
