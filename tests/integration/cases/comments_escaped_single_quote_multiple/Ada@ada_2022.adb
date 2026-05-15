with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("host", AStr ("it's here")),  -- a comment
        AEntry ("port", AInt (80))  -- another
    ];
begin
    null;
end Main;
