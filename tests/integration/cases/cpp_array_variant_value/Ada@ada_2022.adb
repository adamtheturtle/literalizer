with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AInt (1)),
        AEntry ("b", AStr ("x")),
        AEntry ("e", AList'[AInt (1), AInt (2)]),
        AEntry ("f", AMap'[AEntry ("g", AStr ("h"))])
    ];
begin
    null;
end Main;
