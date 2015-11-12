from demo.models import DemoModel
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from renderer.tests import create_superuser, create_image


class WidgetTest(TestCase):
    def test_admin_widget(self):
        username, password = create_superuser()

        c = Client()
        c.login(username=username, password=password)

        r = c.get(reverse('admin:demo_demomodel_changelist'))
        self.assertEqual(r.status_code, 200, (
            'cant access changelist'
        ))

        r = c.get(reverse('admin:demo_demomodel_add'))
        self.assertEqual(r.status_code, 200, (
            'cant access add page'
        ))

        dm = DemoModel(
            master=create_image()
        )
        dm.save()
        r = c.get(reverse('admin:demo_demomodel_change', args=(dm.pk, )))
        self.assertEqual(r.status_code, 200, (
            'cant access change page'
        ))