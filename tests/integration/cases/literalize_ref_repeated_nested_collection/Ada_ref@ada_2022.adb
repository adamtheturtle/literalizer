with A_Stub; use A_Stub;
procedure Main is
    shared : A_Val := AList'[
        AList'[AInt (1), AInt (2)],
        AMap'[AEntry ("value", AInt (1))]
    ];
    my_data : A_Val := AList'[
        shared,
        shared
    ];
begin
    null;
end Main;
