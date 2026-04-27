with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("lint", AList'[AInt (2), AList'[]]),
        AEntry ("test", AList'[AInt (5), AList'[AStr ("compile")]])
    ];
begin
    my_data := AMap'[
        AEntry ("lint", AList'[AInt (2), AList'[]]),
        AEntry ("test", AList'[AInt (5), AList'[AStr ("compile")]])
    ];
end Check;
