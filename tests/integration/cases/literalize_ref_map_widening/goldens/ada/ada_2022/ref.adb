with A_Stub; use A_Stub;
procedure Main is
    string_map : A_Val := AMap'[
        AEntry ("k", AStr ("s"))
    ];
    my_data : A_Val := AList'[
        string_map,
        AMap'[AEntry ("k", AInt (1))]
    ];
begin
    null;
end Main;
