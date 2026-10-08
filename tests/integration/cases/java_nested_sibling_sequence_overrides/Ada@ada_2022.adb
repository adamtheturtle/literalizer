with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AList'[AList'[AInt (1)], AList'[AInt (2)]]),
        AEntry ("b", AList'[AList'[AStr ("x")], AList'[AStr ("y")]])
    ];
begin
    null;
end Main;
