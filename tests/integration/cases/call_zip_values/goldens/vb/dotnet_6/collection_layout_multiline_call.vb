Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Function emit(_call As Object, _zip As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        emit(process("hello"), True)
        emit(process(42), False)
    End Sub
End Module
