from odoo import models,fields

class RaceTeamManagement(models.Model):
    _name='race.team.management'
    _description = 'Race Team Management'
    name=fields.Char()