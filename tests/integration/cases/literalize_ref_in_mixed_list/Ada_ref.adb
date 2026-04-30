with A_Stub; use A_Stub;
procedure Main is
    x : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    my_data : A_Val := AList'[
        x,
        AInt (1),
        AInt (2)
    ];
begin
    null;
end Main;
