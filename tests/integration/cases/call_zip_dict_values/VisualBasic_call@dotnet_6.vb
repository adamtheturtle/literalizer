Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Function emit(_call As Object, _zip As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        emit(process("hello"), New Dictionary(Of String, Object) From {{"a", 1}, {"b", 2}})
        emit(process(42), New Dictionary(Of String, Object) From {{"c", 3}, {"d", 4}})
    End Sub
End Module
