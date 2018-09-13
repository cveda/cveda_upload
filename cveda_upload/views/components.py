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

# CW import
from cubicweb.predicates import anonymous_user
from cubicweb.web import component

# Cubes import
from cubes.piws.views.components import PIWSNavigationtBox
from cubes.rql_upload.views.components import CWUploadBox


class IMAGENCWUploadedBox(CWUploadBox):
    """ Class that generate a left box on the web browser to access all user
        and group uploads.

    .. warning::

        It will NOT appear for anonymous users.
    """

    def render_body(self, w, **kwargs):
        super(IMAGENCWUploadedBox, self).render_body(w, **kwargs)

        rql = ("DISTINCT Any G ORDERBY N WHERE G is CWGroup,"
               " G cwuri ILIKE '%ou=Centres%',"
               " U in_group G, U login '{}', G name N")
        rql = rql.format(self._cw.user.login)
        rset = self._cw.execute(rql)
        for entity in rset.entities():
            #~ if entity.name == 'managers' or entity.name == 'users':
                #~ continue
            href = self._cw.build_url(
                "view",
                rql=("Any X ORDERBY X DESC WHERE X is CWUpload,"
                     " X upload_fields F, F name 'centre',"
                     " F value '{}'".format(entity.name))
            )
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            w(u'<a class="btn btn-primary" href="{0}">'.format(href))
            w(u'<span class="glyphicon glyphicon glyphicon-cloud-upload"></span>')
            w(u'{} uploads</a>'.format(entity.name))
            w(u'</div></div><br/>')


class DashboardsBox(component.CtxComponent):
    """ Class that generate a left box on the web browser
        to access all dashboards (user and centre(s)).

    .. warning::

        It will NOT appear for anonymous users.
    """
    __regid__ = "ctx-dashboards-box"
    __select__ = (component.CtxComponent.__select__ & ~anonymous_user())
    title = _("Dashboards")
    context = "left"
    order = -1

    def render_body(self, w, **kwargs):
        # my dashboard
        href = self._cw.build_url(
            "view", vid="dashboard-view",
            title="My dashboard",
            user=self._cw.user.login)
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'<span class="glyphicon glyphicon glyphicon-list-alt"></span>')
        w(u'My dashboard</a>')
        w(u'</div></div><br/>')

        # centre dashboard
        rql = ("DISTINCT Any G ORDERBY N WHERE G is CWGroup,"
               " G cwuri ILIKE '%ou=Centres%',"
               " U in_group G, U login '{}', G name N")
        rql = rql.format(self._cw.user.login)
        rset = self._cw.execute(rql)
        for entity in rset.entities():
            href = self._cw.build_url(
                "view", vid="dashboard-view",
                title='{} dashboard'.format(entity.name),
                centre=entity.name
            )
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            w(u'<a class="btn btn-primary" href="{0}">'.format(href))
            w(u'<span class="glyphicon glyphicon glyphicon-list-alt"></span>')
            w(u'{} dashboard</a>'.format(entity.name))
            w(u'</div></div><br/>')


def registration_callback(vreg):

    # Update components
    vreg.unregister(PIWSNavigationtBox)
    vreg.register_and_replace(IMAGENCWUploadedBox, CWUploadBox)
    vreg.register(DashboardsBox)
