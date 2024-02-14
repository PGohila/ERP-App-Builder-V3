
class <**Screen_Name**>ListCreateView(APIView):
    def get(self, request):
        records = <**Model_Name**>.objects.all()
        serializer = <**Model_Name**>Serializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = <**Model_Name**>Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class <**Screen_Name**>RetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return <**Model_Name**>.objects.get(pk=pk)
        except <**Model_Name**>.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = <**Model_Name**>Serializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = <**Model_Name**>Serializer(records, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)