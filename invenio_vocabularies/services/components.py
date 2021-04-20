# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Vocabulary components."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.components import \
    ServiceComponent
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from ..records.models import VocabularyType


class VocabularyTypeComponent(ServiceComponent):
    """Set the record's vocabulary type."""

    valid_types_cache = {}

    def _set_type(self, data, record):
        type_id = data.pop('type', None)
        if type_id:
            try:
                if type_id['id'] not in self.valid_types_cache:
                    t = VocabularyType.query.filter_by(id=type_id['id']).one()
                    self.valid_types_cache[type_id['id']] = t
                else:
                    t = self.valid_types_cache[type_id['id']]
                record.type = t
            except NoResultFound:
                raise ValidationError(
                    _('The vocabulary type does not exists.'),
                    field_name='type',
                )

    def create(self, identity, data=None, record=None, **kwargs):
        """Inject vocabulary type to the record."""
        self._set_type(data, record)

    def update(self, identity, data=None, record=None, **kwargs):
        """Inject vocabulary type to the record."""
        self._set_type(data, record)


class PIDComponent(ServiceComponent):
    """PID registration component."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create PID when record is created.."""
        # We create the PID after all the data has been initialized. so that
        # we can rely on having the 'id' and type set.
        self.service.record_cls.pid.create(record)
