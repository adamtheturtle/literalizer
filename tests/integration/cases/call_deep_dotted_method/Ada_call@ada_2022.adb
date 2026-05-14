with A_Stub; use A_Stub;
procedure Main is
    procedure Post (Data : A_Val) is begin null; end Post;
begin
    Post(data => AStr ("hello"));
    Post(data => AInt (42));
    Post(data => ABool (True));
end Main;
