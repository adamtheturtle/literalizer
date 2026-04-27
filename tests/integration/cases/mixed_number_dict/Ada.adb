with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("a", AInt (1)),
        AEntry ("b", AFloat (2.5)),
        AEntry ("c", AInt (3))
    ];
begin
    null;
end Check;
