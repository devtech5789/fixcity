import unittest
import mock


class TestRecaptchaTags(unittest.TestCase):

    def test_recaptcha_html(self):
        from fixcity.bmabr.templatetags import recaptcha_tags
        from django.conf import settings  
        html = recaptcha_tags.recaptcha_html()
        self.failUnless(settings.RECAPTCHA_PUBLIC_KEY in html)
        self.failUnless(html.startswith('<script'))


class TestGoogleTags(unittest.TestCase):

    @mock.patch('fixcity.bmabr.templatetags.google_analytics.settings')
    def test_google_analytics(self, mock_settings):
        from fixcity.bmabr.templatetags import google_analytics
        mock_settings.GOOGLE_ANALYTICS_KEY = 'xyzpdq'
        html = google_analytics.google_analytics()
        self.failUnless('xyzpdq' in html)
        self.failUnless(html.startswith('<script'))

    @mock.patch('fixcity.bmabr.templatetags.google_analytics.settings')
    def test_google_analytics__no_key(self, mock_settings):
        from fixcity.bmabr.templatetags import google_analytics
        mock_settings.GOOGLE_ANALYTICS_KEY = ''
        html = google_analytics.google_analytics()
        self.assertEqual(html, '')


class TestRackverificationTags(unittest.TestCase):

    def test_do_rack_requirements(self):
        parser = mock.Mock()
        token = mock.Mock()
        token.contents.split.return_value = ('rack_requirements', 'as',
                                             'thingy')
        from fixcity.bmabr.templatetags import rackverification_tags
        node = rackverification_tags.do_rack_requirements(parser, token)
        context = {}
        rendered = node.render(context)

        self.assertEqual(rendered, '')
        self.assertEqual(context['thingy'], rackverification_tags.verification_details)

class TestRackHeartTags(unittest.TestCase):

    def _get_node(self, contents):
        from fixcity.bmabr.templatetags import rackheart_tags
        parser = mock.Mock()
        token = mock.Mock()
        token.contents = contents
        node = rackheart_tags.do_can_heart(parser, token)
        return node

    @mock.patch('voting.models.Vote.objects.get_for_user')
    def test_do_can_heart__authenticated(self, mock_get_for_user):
        # Mark this user as having not hearted this rack,
        # without loading real models.
        mock_get_for_user.return_value = None

        bob = mock.Mock()
        bob.is_authenticated.return_value = True
        bob.username = 'bob'

        rack = mock.Mock()
        rack.user = 'not bob'   # You can 'heart' racks if they're not 'yours'

        context = {'bob': bob, 'rack1': rack}
        node = self._get_node('can_heart bob rack1 as canheart')
        rendered = node.render(context)
        self.assertEqual(rendered, u'')
        self.assertEqual(context['canheart'], True)


    def test_do_can_heart__your_own_rack(self):
        bob = mock.Mock()
        bob.is_authenticated.return_value = True
        bob.username = 'bob'
        rack = mock.Mock()
        rack.user = 'bob'  # Can't 'heart' your own racks.
        context = {'bob': bob, 'rack1': rack}
        node = self._get_node('can_heart bob rack1 as canheart')
        node.render(context)
        self.assertEqual(context['canheart'], False)

    def test_do_can_heart__anonymous(self):
        bob = mock.Mock()
        bob.is_authenticated.return_value = False
        context = {'bob': bob, 'rack1': mock.Mock()}
        node = self._get_node('can_heart bob rack1 as canheart')
        rendered = node.render(context)
        self.assertEqual(rendered, u'')
        self.assertEqual(context['canheart'], False)
