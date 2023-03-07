# _author: Coke
# _date: 2023/3/7 10:07

from clientele import api


def update_task_status(body: dict) -> api.request:
    """ 修改任务状态 """

    return api.request(
        'POST',
        '/task/center/status',
        json=body
    )


def new_task_report(body) -> api.request:
    """ 新增测试报告信息 """

    return api.request(
        'POST',
        '/task/report/new',
        json=body,
        exceptions=Exception
    )
