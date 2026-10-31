import logging
from typing import List

from django.db import transaction
from rest_framework import serializers

from eventyay.base.models import Question, Quota, Product, Variation

logger = logging.getLogger(__name__)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "type",
            "required",
            "ask_during_checkin",
            "position",
            "identifier",
            "help_text",
            "items",
            "products",
        )
        read_only_fields = ("id",)

    def validate(self, data):
        """Validate the incoming data.

        The ``products`` field is optional.  When it is omitted we treat it as an
        empty list so that ``clean_products`` receives an iterable instead of
        ``None`` which would raise a ``TypeError`` and result in a 500 error.
        """
        data = super().validate(data)
        # ``products`` may be missing from the payload – default to an empty list.
        products: List[int] = data.get("products", []) or []
        # ``self.instance`` is ``None`` when creating a new object, but the model
        # provides a ``clean_products`` class method that can be called on the
        # model class as well.  ``self.instance`` is used when updating.
        if self.instance is not None:
            self.instance.clean_products(products)
        else:
            Question.clean_products(products)
        # Store the normalised list back into ``data`` so that ``create`` works
        # with the same value.
        data["products"] = products
        return data

    def create(self, validated_data):
        """Create a ``Question`` instance.

        ``products`` is popped with a default empty list to avoid passing ``None``
        to the ``ManyToManyField`` setter.
        """
        products = validated_data.pop("products", []) or []
        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            question.products.set(products)
        return question

    def update(self, instance, validated_data):
        products = validated_data.pop("products", None)
        if products is not None:
            instance.products.set(products or [])
        return super().update(instance, validated_data)


class QuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = (
            "id",
            "name",
            "size",
            "items",
            "variations",
            "products",
        )
        read_only_fields = ("id",)

    def validate(self, data):
        """Validate the incoming data.

        Both ``products`` and ``variations`` are optional.  Missing keys are
        normalised to empty lists before the model's ``clean_*`` helpers are
        invoked.
        """
        data = super().validate(data)
        products: List[int] = data.get("products", []) or []
        variations: List[int] = data.get("variations", []) or []
        if self.instance is not None:
            self.instance.clean_products(products)
            self.instance.clean_variations(variations)
        else:
            Quota.clean_products(products)
            Quota.clean_variations(variations)
        data["products"] = products
        data["variations"] = variations
        return data

    def create(self, validated_data):
        """Create a ``Quota`` instance.

        ``products`` and ``variations`` are popped with defaults of empty lists
        to prevent ``None`` from being passed to the ``ManyToManyField`` setters.
        """
        products = validated_data.pop("products", []) or []
        variations = validated_data.pop("variations", []) or []
        with transaction.atomic():
            quota = Quota.objects.create(**validated_data)
            quota.products.set(products)
            quota.variations.set(variations)
        return quota

    def update(self, instance, validated_data):
        products = validated_data.pop("products", None)
        variations = validated_data.pop("variations", None)
        if products is not None:
            instance.products.set(products or [])
        if variations is not None:
            instance.variations.set(variations or [])
        return super().update(instance, validated_data)

# The rest of the file (e.g., ProductSerializer, VariationSerializer, etc.)
# remains unchanged and is imported elsewhere in the project.
