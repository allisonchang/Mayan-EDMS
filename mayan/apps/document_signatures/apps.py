from __future__ import unicode_literals

import logging

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from common import MayanAppConfig, menu_facet, menu_sidebar

from .hooks import document_pre_open_hook, document_version_post_save_hook
from .links import (
    link_document_signature_delete, link_document_signature_download,
    link_document_signature_upload, link_document_verify
)
from .permissions import (
    permission_document_verify, permission_signature_delete,
    permission_signature_download, permission_signature_upload
)

logger = logging.getLogger(__name__)


class DocumentSignaturesApp(MayanAppConfig):
    app_namespace = 'signatures'
    app_url = 'signatures'
    name = 'document_signatures'
    test = True
    verbose_name = _('Document signatures')

    def ready(self):
        super(DocumentSignaturesApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        DocumentVersion.register_post_save_hook(
            1, document_version_post_save_hook
        )
        DocumentVersion.register_pre_open_hook(1, document_pre_open_hook)

        ModelPermission.register(
            model=Document, permissions=(
                permission_document_verify, permission_signature_delete,
                permission_signature_download, permission_signature_upload,
            )
        )

        menu_facet.bind_links(
            links=(link_document_verify,), sources=(Document,)
        )
        menu_sidebar.bind_links(
            links=(
                link_document_signature_upload,
                link_document_signature_download,
                link_document_signature_delete
            ), sources=(
                'signatures:document_verify',
                'signatures:document_signature_upload',
                'signatures:document_signature_download',
                'signatures:document_signature_delete'
            )
        )
