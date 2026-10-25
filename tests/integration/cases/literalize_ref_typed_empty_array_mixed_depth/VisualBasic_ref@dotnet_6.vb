Imports System.Collections.Generic
Module Check
    Dim Shallow = New Object() {}
    Dim Deep = New Object() {
        New String() {}
    }
    Dim my_data = New Object() {
        Shallow,
        Deep
    }
End Module
