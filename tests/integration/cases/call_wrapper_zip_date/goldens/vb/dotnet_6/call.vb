Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Function emit(_call As Object, _zip As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        emit(process(1), New DateOnly(2024, 1, 15))
    End Sub
End Module
