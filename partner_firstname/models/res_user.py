# -*- coding: utf-8 -*-
# © 2013 Nicolas Bessi (Camptocamp SA)
# © 2014 Agile Business Group (<http://www.agilebg.com>)
# © 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from openerp import api, models


_logger = logging.getLogger(__name__)


class ResUser(models.Model):
    _inherit = 'res.users'

    @api.model
    def default_get(self, fields_list):
        """Invert name when getting default values."""
        result = super(ResUser, self).default_get(fields_list)

        partner_model = self.env['res.partner']
        inverted = partner_model._get_inverse_name(
            partner_model._get_whitespace_cleaned_name(result.get("name", "")),
            result.get("is_company", False))

        for field in inverted.keys():
            if field in fields_list:
                result[field] = inverted.get(field)

        return result

    @api.one
    @api.onchange("firstname", "lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        self.name = self.partner_id._get_computed_name(
            self.lastname, self.firstname)
