# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from keystoneclient import base
from keystoneclient.v2_0 import roles
from tests import utils


class BaseTest(utils.TestCase):

    def test_resource_repr(self):
        r = base.Resource(None, dict(foo="bar", baz="spam"))
        self.assertEqual(repr(r), "<Resource baz=spam, foo=bar>")

    def test_getid(self):
        self.assertEqual(base.getid(4), 4)

        class TmpObject(object):
            id = 4
        self.assertEqual(base.getid(TmpObject), 4)

    def test_resource_lazy_getattr(self):
        self.client.get = self.mox.CreateMockAnything()
        self.client.get('/OS-KSADM/roles/1').AndRaise(AttributeError)
        self.mox.ReplayAll()

        f = roles.Role(self.client.roles, {'id': 1, 'name': 'Member'})
        self.assertEqual(f.name, 'Member')

        # Missing stuff still fails after a second get
        self.assertRaises(AttributeError, getattr, f, 'blahblah')

    def test_eq(self):
        # Two resources of the same type with the same id: equal
        r1 = base.Resource(None, {'id': 1, 'name': 'hi'})
        r2 = base.Resource(None, {'id': 1, 'name': 'hello'})
        self.assertEqual(r1, r2)

        # Two resoruces of different types: never equal
        r1 = base.Resource(None, {'id': 1})
        r2 = roles.Role(None, {'id': 1})
        self.assertNotEqual(r1, r2)

        # Two resources with no ID: equal if their info is equal
        r1 = base.Resource(None, {'name': 'joe', 'age': 12})
        r2 = base.Resource(None, {'name': 'joe', 'age': 12})
        self.assertEqual(r1, r2)
