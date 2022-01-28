# Copyright (C) 2018 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import requests
import os
import firebase_admin
from odoo import api, fields, models
from firebase_admin import firestore

default_app = firebase_admin.initialize_app()
db = firestore.client()

endpoint = os.environ.get('MIDDLEWARE_URL')

_logger = logging.getLogger(__name__)

class FSMOrder(models.Model):
    _inherit = "fsm.order"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        _logger.info("vals: %s", vals)
        doc_ref = db.collection(u'jobs').document(vals['name'])
        keys_values = vals.items()
        doc_ref.set({str(key): str(value) for key, value in keys_values})
        return res

    @api.onchange("location_id")
    def onchange_location_id(self):
        res = super().onchange_location_id()
        return res
