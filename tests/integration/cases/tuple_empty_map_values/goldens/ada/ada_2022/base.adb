with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("filled", AList'[AInt (1), AStr ("value")]),
        AEntry ("empty", AList'[])
    ];
begin
    null;
end Main;
