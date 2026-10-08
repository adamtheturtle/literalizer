with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("d", AList'[AMap'[AEntry ("a", AList'[AMap'[AEntry ("b", AList'[AInt (1), AList'[AFloat (2.5), AList'[AStr ("x"), AList'[ABool (True)]]]])]])]])
    ];
begin
    null;
end Main;
