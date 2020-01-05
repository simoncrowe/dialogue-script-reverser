"""Serialisation and deserialisation of dialogue data."""

from marshmallow import fields, post_load, Schema

from .data import Choice, Node


class ChoiceSchema(Schema):

    target = fields.Str(data_key="Target")
    player = fields.Str(data_key="Player")

    @post_load
    def make_choice(self, data, **kwargs):
        return Choice(**data)


class NodeSchema(Schema):
    
    id = fields.Str(data_key='ID')
    npc = fields.Str(data_key='NPC')
    choices = fields.Nested(ChoiceSchema, many=True, data_key="Choices")

    @post_load
    def make_node(self, data, **kwargs):
        return Node(**data)
        
