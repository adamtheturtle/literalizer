with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("x", AInt (1)), AEntry ("y", AFloat (2.5))],
        AMap'[AEntry ("x", AInt (3)), AEntry ("y", AFloat (4.0))]
    ];
begin
    my_data := AList'[
        AMap'[AEntry ("x", AInt (1)), AEntry ("y", AFloat (2.5))],
        AMap'[AEntry ("x", AInt (3)), AEntry ("y", AFloat (4.0))]
    ];
end Main;
