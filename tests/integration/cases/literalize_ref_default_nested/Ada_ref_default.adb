with A_Stub; use A_Stub;
procedure Main is
    my_var : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    item_var : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    my_data : A_Val := AMap'[
        AEntry ("key", my_var),
        AEntry ("items", AList'[item_var, AMap'[AEntry ("fallback", AStr ("value"))]])
    ];
begin
    null;
end Main;
