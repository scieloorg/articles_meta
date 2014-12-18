import unittest

from pyramid import testing
import pyramid.httpexceptions as exc

from articlemeta import articlemeta


class ViewsTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_get_request_limit_param_by_default(self):
        """
        test default behavior of the helper function: _get_request_limit_param
        - only positive limits are allowed
        - if request.limit is greater than default_limit, will return the default limit (1000)
        """
        # set a list of tuples (limit requested, limit expected in response)
        limits = [(1,1), (10, 10), (1000, 1000), (2000, 1000), (12000, 1000)]

        for req_limit, resp_limit in limits:
            request = testing.DummyRequest(params={'limit': req_limit})
            result_limit = articlemeta._get_request_limit_param(request)
            self.assertEqual(result_limit, resp_limit)

    def test_get_request_limit_param_with_new_default_limit(self):
        """
        define new default limit, that will be the top value returned
        """
        new_default_limit = 200
        # set a list of tuples (limit requested, limit expected in response)
        limits = [
            (1,1), (10, 10), (1000, new_default_limit),
            (2000, new_default_limit), (12000, new_default_limit)
        ]

        for req_limit, resp_limit in limits:
            request = testing.DummyRequest(params={'limit': req_limit})
            result_limit = articlemeta._get_request_limit_param(request, default_limit=new_default_limit)
            self.assertEqual(result_limit, resp_limit)

    def test_get_request_limit_param_with_limit_zero_NOT_allowed(self):
        """
        By default the _get_request_limit_param will NOT accept request it limit <= 0
        So here test that a BadRequestException is raised
        """
        limits = [(0,0), (-1, -1), (-1000, -1000)]

        for req_limit, resp_limit in limits:
            request = testing.DummyRequest(params={'limit': req_limit})
            self.assertRaises(exc.HTTPBadRequest,
                              articlemeta._get_request_limit_param,
                              request)

    def test_get_request_limit_param_with_limit_zero_allowed(self):
        """
        _get_request_limit_param can accept request it limit <= 0
        So here test that and returns a valid number
        """
        limits = [(0,0), (-1, -1), (-1000, -1000)]

        for req_limit, resp_limit in limits:
            request = testing.DummyRequest(params={'limit': req_limit})
            result_limit = articlemeta._get_request_limit_param(request, only_positive_limit=False)
            self.assertEqual(result_limit, resp_limit)

    def test_get_request_limit_param__can_ignore_default_limit(self):
        """
        In some case every requested limit, must be the returned,
        even if is bigger than default_limit.
        """
        # set a list of tuples (limit requested, limit expected in response)
        limits = [(1,1), (10, 10), (1000, 1000), (2000, 2000), (12000, 12000)]

        for req_limit, resp_limit in limits:
            request = testing.DummyRequest(params={'limit': req_limit})
            result_limit = articlemeta._get_request_limit_param(request, force_max_limit_to_default=False)
            self.assertEqual(result_limit, resp_limit)
