# _author: Coke
# _date: 2023/8/18 13:51

from clientele import api


def get_mock_domain_list(project_id) -> api.request:
    """ 获取域名列表的信息 """

    body = dict(
        page=1,
        pageSize=99999,
        projectId=project_id
    )

    return api.request(
        'GET',
        '/mock/domain/list',
        json=body
    ).get('items')


def get_mock_api_list(project_id) -> api.request:
    """ 获取接口列表的信息 """

    body = dict(
        page=1,
        pageSize=99999,
        projectId=project_id
    )

    return api.request(
        'GET',
        '/mock/api/list',
        json=body
    ).get('items')
