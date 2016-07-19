from __future__ import absolute_import

from rest_framework import serializers

from modelcluster.models import get_all_child_relations

from wagtail.contrib import wagtailapi as wapi
from wagtail.contrib.wagtailapi.endpoints import ImagesAPIEndpoint, DocumentsAPIEndpoint
from wagtail.contrib.wagtailapi.router import WagtailAPIRouter
from wagtail.contrib.wagtailapi.serializers import get_serializer_class
from wagtail.wagtailimages.models import Image


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, image):
        return image.file.url

    class Meta:
        model = Image
        fields = ('id', 'title', 'url', 'height', 'width')


class RelatedField(wapi.serializers.RelatedField):
    models_mapping = {
        Image: ImageSerializer,
    }

    def to_representation(self, value):
        if value.__class__ in self.models_mapping:
            serializer_class = self.models_mapping[value.__class__]
            return serializer_class(value).data
        elif hasattr(value.__class__, 'api_fields'):
            child_fields = value.__class__.api_fields
            serializer_class = get_serializer_class(value.__class__, child_fields, BaseSerializer)
            serializer = serializer_class(context=self.context)
            return serializer.to_representation(value)
        else:

            return super(RelatedField, self).to_representation(value)


class ChildRelationField(wapi.serializers.ChildRelationField):
    def to_representation(self, value):
        serializer_class = get_serializer_class(value.model, self.child_fields, BaseSerializer)
        serializer = serializer_class(context=self.context)

        return [
            serializer.to_representation(child_object)
            for child_object in value.all()
        ]


class BaseSerializer(wapi.serializers.BaseSerializer):
    serializer_related_field = RelatedField


class PageSerializer(wapi.serializers.PageSerializer):
    serializer_related_field = RelatedField

    def build_relational_field(self, field_name, relation_info):
        # Find all relation fields that point to child class and make them use
        # the ChildRelationField class.
        if relation_info.to_many:
            model = getattr(self.Meta, 'model')
            child_relations = {
                child_relation.field.rel.related_name: child_relation.related_model
                for child_relation in get_all_child_relations(model)
            }

            if field_name in child_relations and hasattr(child_relations[field_name], 'api_fields'):
                return ChildRelationField, {'child_fields': child_relations[field_name].api_fields}

        return super(PageSerializer, self).build_relational_field(field_name, relation_info)


class PageAPIEndpoint(wapi.endpoints.PagesAPIEndpoint):
    base_serializer_class = PageSerializer


def serialize(obj, context=None):
    child_fields = obj.__class__.api_fields
    serializer_class = get_serializer_class(obj.__class__, child_fields, BaseSerializer)
    serializer = serializer_class(context=context)
    return serializer.to_representation(obj)


router = WagtailAPIRouter('api')
router.register_endpoint('pages', PageAPIEndpoint)
router.register_endpoint('images', ImagesAPIEndpoint)
router.register_endpoint('documents', DocumentsAPIEndpoint)
