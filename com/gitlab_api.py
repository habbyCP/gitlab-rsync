import time

from gevent import monkey

from com.logger import logger

monkey.patch_all()

import requests
from com.loadconf import Config
from functools import lru_cache


class GitlabApi:
    gitlab_url = ""
    header = {}

    def __init__(self):
        self.gitlab_url = "%s://%s" % (Config.target_protocol, Config.target_domain)
        self.header = {"PRIVATE-TOKEN": Config.target_token}

    @lru_cache(maxsize=1)
    def GetProjectList(self, salt=0):
        # salt传入的key是一个随机数，用于刷新缓存
        GroupList = {}
        for i in range(1, 100):
            params = {"per_page": 100, "page": i}
            data = requests.get(self.gitlab_url + "/api/v4/groups", headers=self.header, params=params)
            if len(data.json()) == 0:
                break
            for g in data.json():
                GroupList[g["full_path"]] = g["id"]
        return GroupList

    def MatchAndGreate(self, group, pid, group_path):
        # 获取所有的group，缓存15分钟
        GroupList = self.GetProjectList(int(time.time()) // 900)
        # 判断group存在不，如果存在则返回ID,不存在则创建,然后返回ID
        if group_path in GroupList:
            # print("命中 : %s id %s" % (group_path, GroupList[group_path]))
            return GroupList[group_path]
        else:
            params = {"name": group, "path": group}
            if pid > 0:
                params["parent_id"] = pid
            data = requests.post(self.gitlab_url + "/api/v4/groups", headers=self.header, params=params)
            if data.status_code == 201:
                GroupList[group] = data.json()["id"]
                return data.json()["id"]
            else:
                logger.error("创建group失败: %s" % data.text)
                return 0

    def CreateGroupByLongPath(self, path):
        # 通过长路径创建group
        # 1.通过/分割path
        # 2.通过/分割后的每一项去创建group
        # 3.创建完毕后返回最后一项的ID
        path_list = path.split("/")
        pid = 0
        group_path = ""
        for i in path_list:
            group_path = group_path + "/" + i
            pid = self.MatchAndGreate(i, pid, group_path.strip("/"))
            if pid == 0:
                # 创建失败
                return 0
        return pid


GitlabApi = GitlabApi()