with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("lint", AList'[AInt (2), AList'[]]),
        AEntry ("test", AList'[AInt (5), AList'[AStr ("compile")]])
    ];
begin
    null;
end Main;
