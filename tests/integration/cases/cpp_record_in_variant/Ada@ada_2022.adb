with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("h", AList'[AInt (1), AStr ("a"), AList'[AInt (2), AStr ("b")], AMap'[AEntry ("k", AList'[ABool (True)])]])
    ];
begin
    null;
end Main;
