Imports System.Collections.Generic
Module Check
    Function record(value As Object) As Object
        Return Nothing
    End Function
    Function flush(count As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        record(42)
        flush(3)
    End Sub
End Module
