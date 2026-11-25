with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("cr", AStr ("a" & Character'Val(13) & "b")),
        AEntry ("crlf", AStr ("a" & Character'Val(13) & Character'Val(10) & "b")),
        AEntry ("lf", AStr ("a" & Character'Val(10) & "b"))
    ];
begin
    null;
end Main;
