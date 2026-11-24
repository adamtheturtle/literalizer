with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("b", ANull),
        AEntry ("a", AMap'[AEntry ("y", AList'[AFloat (1.0)]), AEntry ("x", ABool (False))])
    ];
begin
    null;
end Main;
