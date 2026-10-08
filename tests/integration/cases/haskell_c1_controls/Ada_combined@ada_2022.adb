with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AStr (Character'Val(127) & "0" & Character'Val(194) & Character'Val(128) & "a" & Character'Val(194) & Character'Val(159) & "F");
begin
    my_data := AStr (Character'Val(127) & "0" & Character'Val(194) & Character'Val(128) & "a" & Character'Val(194) & Character'Val(159) & "F");
end Main;
