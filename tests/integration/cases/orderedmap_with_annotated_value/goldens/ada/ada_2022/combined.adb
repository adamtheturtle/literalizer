with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AList'[]),
        AEntry ("b", AInt (1))
    ];
begin
    my_data := AMap'[
        AEntry ("a", AList'[]),
        AEntry ("b", AInt (1))
    ];
end Main;
