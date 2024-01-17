from rest_framework import serializers

class TotalSumSerializer(serializers.Serializer):
    total_sum = serializers.DecimalField(max_digits=15, decimal_places=2)
    count_reservations = serializers.IntegerField()
    average_price = serializers.DecimalField(max_digits=15, decimal_places=2)
    most_common_model = serializers.CharField(allow_null=True, required=False)
    most_common_brand = serializers.CharField(allow_null=True, required=False)
    average_duration_days = serializers.IntegerField(required=False)
