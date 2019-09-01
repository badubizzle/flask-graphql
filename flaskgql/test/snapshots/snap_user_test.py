# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_get_all_users 1'] = {
    'data': {
        'allUsers': {
            'edges': [
                {
                    'node': {
                        'uuid': '915476cb-26d7-49f2-aa3d-cd64b435ff59'
                    }
                }
            ]
        }
    }
}

snapshots['test_create_user_with_user_name 1'] = b'{"errors":[{"message":"Username already exists","locations":[{"line":3,"column":11}],"path":["createUser"]}],"data":{"createUser":null}}'
