"""
Serializers for suppliers app.
"""

from rest_framework import serializers

from apps.suppliers.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Supplier model."""

    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Supplier
        fields = [
            "id",
            "code",
            "name",
            "contact_person",
            "email",
            "phone",
            "address",
            "city",
            "country",
            "tax_id",
            "website",
            "status",
            "status_display",
            "payment_terms",
            "notes",
            "rating",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
