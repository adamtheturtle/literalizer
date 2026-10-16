with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("type", AStr ("create")), AEntry ("name", AStr ("a"))],
        AMap'[AEntry ("type", AStr ("update")), AEntry ("name", AStr ("b"))]
    ];
begin
    null;
end Main;
