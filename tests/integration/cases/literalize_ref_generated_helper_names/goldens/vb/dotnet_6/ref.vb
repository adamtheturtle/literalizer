Imports System.Collections.Generic
Module Check
    Dim Std = New Dictionary(Of String, Object) From {
        {"a", 1}
    }
    Dim Arena = New Dictionary(Of String, Object) From {
        {"a", 1}
    }
    Dim Allocator = New Dictionary(Of String, Object) From {
        {"a", 1}
    }
    Dim my_data = New Object() {
        Std,
        Arena,
        Allocator
    }
End Module
