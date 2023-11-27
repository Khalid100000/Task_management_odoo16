# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import http 
from odoo.http import request
from datetime import datetime, timedelta
import re
import json
from urllib.request import urlopen
import requests
from psycopg2 import sql


class WebsiteTrack(models.Model):
    _inherit = 'website.track'
    ip_address=fields.Char(string='Ip Address')
    ip_address_country=fields.Char(string='Ip Country',compute='_compute_country',store=False)
    
    
    @api.depends('ip_address')
    def _compute_country(self):
        for rec in self:
            forwarded_for=rec.ip_address
            response = requests.get(f'http://ipinfo.io/{forwarded_for}/json')
            
            data = response.json()
            print('Computing the country for ip address----------------------------------------------------')
            print(data)

            if 'country' in data:
                cnt = data['country']
                print(f'The IP address {forwarded_for} is located in {cnt}.')
                rec.ip_address_country = data['country']
            else:
                rec.ip_address_country='N/A'


class Visit(models.Model):
    _inherit = 'website.visitor'
    def _get_ip_address(self):
        forwarded_for = request.httprequest.headers.get('X-Forwarded-For')
        print(f'Forwarded_for IP ADDRESS: {forwarded_for}')
        return forwarded_for

    ip_address=fields.Char(string='Last IP',readonly=True)
    ip_address_hostname=fields.Char(compute='_compute_country',store=False)
    ip_address_country=fields.Char(string='Last Ip Country',compute='_compute_country',store=False)
    ip_address_city=fields.Char(compute='_compute_country',store=False)
    ip_address_region=fields.Char(compute='_compute_country',store=False)

    
    
    @api.depends('ip_address')
    def _compute_country(self):
        for rec in self:
            forwarded_for=rec.ip_address
            response = requests.get(f'http://ipinfo.io/{forwarded_for}/json')
            
            data = response.json()
            print('Computing the country for ip address----------------------------------------------------')
            print(data)

            if 'country' in data:
                cnt = data['country']
                print(f'The IP address {forwarded_for} is located in {cnt}.')
                rec.ip_address_country = data['country']
            else:
                rec.ip_address_country='N/A'

            if 'hostname' in data:
                rec.ip_address_hostname =data['hostname']
            else:
                rec.ip_address_hostname ='N/A'

            if 'city' in data:
                rec.ip_address_city =data['city']
            else:
                rec.ip_address_city ='N/A'

            if 'region' in data:
                rec.ip_address_region =data['region']
            else:
                rec.ip_address_region ='N/A'


    def _handle_webpage_dispatch(self, website_page):
        """ Create a website.visitor if the http request object is a tracked
        website.page or a tracked ir.ui.view.
        Since this method is only called on tracked elements, the
        last_connection_datetime might not be accurate as the visitor could have
        been visiting only untracked page during his last visit."""

        url = request.httprequest.url
        ip = request.httprequest.headers.get('X-Forwarded-For')
        website_track_values = {'url': url}
        if website_page:
            website_track_values['page_id'] = website_page.id
            website_track_values['ip_address'] = ip
        self._get_visitor_from_request(force_create=True, force_track_values=website_track_values)


    def _upsert_visitor(self, access_token, force_track_values=None):
        """ Based on the given `access_token`, either create or return the
        related visitor if exists, through a single raw SQL UPSERT Query.

        It will also create a tracking record if requested, in the same query.

        :param access_token: token to be used to upsert the visitor
        :param force_track_values: an optional dict to create a track at the
            same time.
        :return: a tuple containing the visitor id and the upsert result (either
            `inserted` or `updated).
        """
        create_values = {
            'ip_address' : request.httprequest.headers.get('X-Forwarded-For'),
            'access_token': access_token,
            'lang_id': request.lang.id,
            # Note that it's possible for the GEOIP database to return a country
            # code which is unknown in Odoo
            'country_code': request.geoip.get('country_code'),
            'website_id': request.website.id,
            'timezone': self._get_visitor_timezone() or None,
            'write_uid': self.env.uid,
            'create_uid': self.env.uid,
            # If the access_token is not a 32 length hexa string, it means that the
            # visitor is linked to a logged in user, in which case its partner_id is
            # used instead as the token.
            'partner_id': None if len(str(access_token)) == 32 else access_token,
        }
        print(f'Create_values are: {create_values}')
        query = """
            INSERT INTO website_visitor (
                ip_address, partner_id, access_token, last_connection_datetime, visit_count, lang_id,
                website_id, timezone, write_uid, create_uid, write_date, create_date, country_id)
            VALUES (
                %(ip_address)s,%(partner_id)s, %(access_token)s, now() at time zone 'UTC', 1, %(lang_id)s,
                %(website_id)s, %(timezone)s, %(create_uid)s, %(write_uid)s,
                now() at time zone 'UTC', now() at time zone 'UTC', (
                    SELECT id FROM res_country WHERE code = %(country_code)s
                )
            )
            ON CONFLICT (access_token)
            DO UPDATE SET
                last_connection_datetime=excluded.last_connection_datetime,
                visit_count = CASE WHEN website_visitor.last_connection_datetime < NOW() AT TIME ZONE 'UTC' - INTERVAL '8 hours'
                                    THEN website_visitor.visit_count + 1
                                    ELSE website_visitor.visit_count
                                END
            RETURNING id, CASE WHEN create_date = now() at time zone 'UTC' THEN 'inserted' ELSE 'updated' END AS upsert
        """
        if force_track_values:
            create_values['url'] = force_track_values['url']
            create_values['page_id'] = force_track_values.get('page_id')
            query = sql.SQL("""
                WITH visitor AS (
                    {query}, %(url)s AS url, %(page_id)s AS page_id, %(ip_address)s AS ip_address
                ), track AS (
                    INSERT INTO website_track (visitor_id, ip_address, url, page_id, visit_datetime)
                    SELECT  id, ip_address, url, page_id::integer, now() at time zone 'UTC' FROM visitor
                )
                SELECT id, upsert from visitor;
            """).format(query=sql.SQL(query))

        self.env.cr.execute(query, create_values)
        return self.env.cr.fetchone()
    

    def _update_visitor_last_visit(self):
        date_now = datetime.now()
        forwarded_for = request.httprequest.headers.get('X-Forwarded-For')

        query = "UPDATE website_visitor SET "
        if self.last_connection_datetime < (date_now - timedelta(hours=8)):
            query += "visit_count = visit_count + 1,"
        query += """
            last_connection_datetime = %s
            ,ip_address = %s
            WHERE id IN (
                SELECT id FROM website_visitor WHERE id = %s
                FOR NO KEY UPDATE SKIP LOCKED
            )
        """
        self.env.cr.execute(query, (date_now,forwarded_for, self.id), log_exceptions=False)

                
