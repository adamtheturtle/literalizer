Imports System.Collections.Generic
Module Check
    Function process() As Object
        Return Nothing
    End Function
    Function emit(_arg As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        emit(process())
        emit(process())
    End Sub
End Module
