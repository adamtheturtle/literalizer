Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Function emit(_arg As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        emit(process(42))
    End Sub
End Module
