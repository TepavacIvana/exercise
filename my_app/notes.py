import marshmallow
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class CreateNoteSchema(Schema):
    title = fields.Str(required=True, validate=Length(max=20))
    note = fields.Str(required=True, validate=Length(max=100))
    user_id = fields.Int(required=True, validate=Range(min=1))

    @marshmallow.validates_schema()
    def validate_object(self, data, **kwargs):
        for word in ['unbelievable', 'impossible', 'undoable', 'can not', 'would not']:
            if word.upper() in data['note'].upper():
                raise marshmallow.ValidationError(
                    'Value should not contain forbidden words',
                    'note'
                )


class UpdateNoteSchema(Schema):
    title = fields.Str(partial=True, validate=Length(max=20))
    note = fields.Str(partial=True, validate=Length(max=100))
    user_id = fields.Int(partial=True, validate=Range(min=1))
    time_created = fields.Str(partial=True)
    time_updated = fields.Str(partial=True)

    @marshmallow.validates_schema()
    def validate_object(self, data, **kwargs):
        if data.get('note'):
            for word in ['unbelievable', 'impossible', 'undoable', 'can not', 'would not']:
                if word.upper() in data['note'].upper():
                    raise marshmallow.ValidationError(
                        'Value should not contain forbidden words',
                        'note'
                    )
