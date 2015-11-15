from demo.models import DemoModel
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from renderer.tests import create_superuser, create_image


def create_demo_model():
    dm = DemoModel(
        master=create_image()
    )
    dm.save()
    return dm


class WidgetTest(TestCase):
    def test_admin_widget(self):
        username, password = create_superuser()
        dm = create_demo_model()

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

        r = c.get(reverse('admin:demo_demomodel_change', args=(dm.pk,)))
        self.assertEqual(r.status_code, 200, (
            'cant access change page'
        ))

    def test_demo_views(self):
        create_demo_model()

        c = Client()
        r = c.get(reverse('demo:index'))
        self.assertEqual(r.status_code, 200, (
            'cant access index page'
        ))

        r = c.get(reverse('demo:ratio'))
        self.assertEqual(r.status_code, 200, (
            'cant access ratio page'
        ))

        r = c.get(reverse('demo:random'))
        self.assertEqual(r.status_code, 200, (
            'cant access random page'
        ))

        r = c.get(reverse('demo:filters'))
        self.assertEqual(r.status_code, 200, (
            'cant access filters page'
        ))
        
