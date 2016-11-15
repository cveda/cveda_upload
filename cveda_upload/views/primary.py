# -*- coding: utf-8 -*-

# Copyright (c) 2013-2016 CEA
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

# CW import
from cubicweb.web.views.primary import PrimaryView
from cubicweb.predicates import is_instance
from cubes.rql_upload.views.primary import CWUploadPrimaryView


class Imagen_CWUploadPrimaryView(PrimaryView):
    """
    """

    __select__ = PrimaryView.__select__ & is_instance("CWUpload")

    def call(self, rset=None):
        eUpload = self.cw_rset.get_entity(0, 0)
        self.w(u'<div class="page-header">')
        self.w(u'<h2>')
        if eUpload.status == 'Quarantine':
            self.w(u"<span class='glyphicon glyphicon-cog' />")
        elif eUpload.status == 'Rejected':
            self.w(u"<span class='glyphicon glyphicon-remove' />")
        elif eUpload.status == 'Validated':
            self.w(u"<span class='glyphicon glyphicon-ok' />")
        else:
            self.w(u"<span class='glyphicon glyphicon-cloud-upload' />")
        self.w(u' {}</h2>'.format(eUpload.dc_title()))
        self.w(u'</div>')

        self.w(u'<div>')
        self.w(u'<h3>Status</h3>')
        self.w(u'<b>{}</b>'.format(eUpload.status))
        print 'error: {}'.format(eUpload.error)
        if eUpload.error:
            self.w(u'<div class="panel panel-danger">{}</div>'.format(
                eUpload.error))
        self.w(u'</div>')

        self.w(u'<div>')
        self.w(u'<h3>Fields</h3>')
        self.w(u'<table class="upload-table">')
        self.w(u'<tr><th>Name</th><th>Value</th></tr>')
        for eField in sorted(eUpload.upload_fields,
                             key=lambda field: field.name):
            self.w(u'<tr><td>{0}</td><td>{1}</td></tr>'.format(
                   eField.label, eField.value))
        self.w(u'</table>')
        self.w(u'</div>')

        self.w(u'<div>')
        self.w(u'<h3>Files</h3>')
        self.w(u'<table class="upload-table">')
        self.w(u'<tr><th>Name</th><th>SHA1</th></tr>')
        for eFile in sorted(eUpload.upload_files,
                            key=lambda field: field.name):
            self.w(u'<tr><td>{0}</td><td>{1}</td></tr>'.format(
                   eFile.data_name, eFile.data_sha1hex))
        self.w(u'</table>')
        self.w(u'</div>')


def registration_callback(vreg):
    """ Register the tuned primary views.
    """

    vreg.register_and_replace(Imagen_CWUploadPrimaryView, CWUploadPrimaryView)
