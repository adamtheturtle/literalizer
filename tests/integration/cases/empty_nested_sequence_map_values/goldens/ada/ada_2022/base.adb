with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("alpha", AList'[AInt (2), AList'[]]),
        AEntry ("beta", AList'[AInt (5), AList'[AStr ("x")]])
    ];
begin
    null;
end Main;
