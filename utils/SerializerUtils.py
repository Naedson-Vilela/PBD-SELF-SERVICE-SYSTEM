
def combine_serializer_errors(list_serializers):
    combined_errors = []
    for serializer in list_serializers:
        serializer.is_valid()
        if serializer.errors:
            combined_errors.append(serializer.errors)
    return combined_errors

