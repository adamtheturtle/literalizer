Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Function emit(_call As Object, _zip As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        emit(process(1), "2024-01-15T12:00:00")
    End Sub
End Module
