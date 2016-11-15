# -*- coding: utf-8 -*-

# Copyright (c) 2016 CEA
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# System import
from cgi import parse_qs

# CW import
from cubicweb.view import View


class DashboardView(View):
    """ View to display subject, time point dashboard under user or centre
    """

    __regid__ = "dashboard-view"
    title = _("Dashboard")

    def call(self, **kwargs):
        # get parameters
        path = self._cw.relative_path()
        if "?" in path:
            path, param = path.split("?", 1)
            kwargs.update(parse_qs(param))
            print kwargs
        # query data
        rql = "Any UP ORDERBY UP DESC WHERE UP is CWUpload,"
        if 'user' in kwargs.keys():
                rql += " UP created_by U, U login '{}'".format(
                    kwargs['user'][0])
        else:
            rql += (" UP upload_fields F, F name 'centre',"
                    " F value = '{}'".format(kwargs['centre'][0]))
        rset = self._cw.execute(rql)

        # compute data
        data = {}
        forms = []
        tps = []
        for entity in rset.entities():
            form = entity.form_name
            forms.append(form)
            sid = entity.get_field_value('sid')
            tp = entity.get_field_value('time_point')
            tps.append(tp)
            status = entity.status
            centre = entity.get_field_value('centre')
            if not sid in data.keys():
                data[sid] = {}
            if not tp in data[sid].keys():
                data[sid][tp] = {}
            if not form in data[sid][tp].keys():
                data[sid][tp][form] = []
            data[sid][tp][form].append(
                (status, centre, entity.dc_creator(), entity.eid))

        forms = list(set(forms))
        forms.sort()
        tps = list(set(tps))
        tps.sort()

        # write title
        self.w(u'<div class="panel-heading">')
        self.w(u'<h1>{}</h1>'.format(kwargs['title'][0]))
        self.w(u'</div>')

        # write dashboard

        self.w(u'<div class="panel-body">')
        self.w(u'<table>')
        self.w(u'<theader><tr>')
        self.w(u"<th rowspan='2'>Subject ID</th>")
        for tp in tps:
            self.w(u"<th colspan='{}'>{}</th>".format(len(forms), tp))
        self.w(u'</tr><tr>')
        for tp in tps:
            for form in forms:
                self.w(u'<th>{}</th>'.format(form))
        self.w(u'</tr></theader>')
        self.w(u'<tbody>')
        for sid in data.keys():
            self.w(u'<tr>')
            self.w(u'<td>{}</td>'.format(sid))
            for tp in tps:
                for form in forms:
                    if tp in data[sid].keys():
                        if form in data[sid][tp].keys():
                            status, centre, user, eid = data[sid][tp][form][0]
                            color = ''
                            if status == 'Quarantine':
                                    color = '#336699'
                            elif status == 'Rejected':
                                color = '#800000'
                            elif status == 'Validated':
                                color = '#008080'
                            else:
                                color = '#FFFFFF'
                            self.w(u"<td style='background-color:{}'>".format(
                                color))

                            for nuple in data[sid][tp][form]:
                                status, centre, user, eid = nuple
                                href = self._cw.build_url(
                                    "view",
                                    rql=("Any U WHERE U is CWUpload"
                                         ", U eid '{}'".format(eid))
                                )
                                icon = ''
                                if status == 'Quarantine':
                                    icon = 'glyphicon-cog'
                                elif status == 'Rejected':
                                    icon = 'glyphicon-remove'
                                elif status == 'Validated':
                                    icon = 'glyphicon-ok'
                                else:
                                    icon = 'glyphicon-question-sign'
                                self.w(
                                    (u"<a href='{}'>"
                                     " <span class='glyphicon {}'"
                                     " title='{} : {}' /><a/>").format(
                                        href, icon, centre, user)
                                )
                            self.w(u'</td>')
                        else:
                            self.w(u'<td/>')
                    else:
                        self.w(u'<td/>')
            self.w(u'</tr>')
        self.w(u'</tbody>')
        self.w(u'</table>')
        self.w(u'</div>')
