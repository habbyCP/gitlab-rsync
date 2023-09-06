import json
import time

from flask import Blueprint

MainPage = Blueprint('admin', __name__, )


@MainPage.route("/api/init_menu", methods=["GET"])
def initMenu():
    init_data = {"homeInfo": {}, "logoInfo": {}, "menuInfo": {}, "userInfo": {}}
    homeInfo = {"title": "首页", "href": "/setting/page?v"+str(time.time())}
    logoInfo = {"title": "G R", "image": "/static/images/logo.png", "href": ""}
    menuInfo = [
        {
              "title": "gitlab同步配置设置",
              "href": "/setting/page",
              "icon": "fa fa-tachometer",
              "target": "_self"
            },
        {
            "title": "业务配置",
            "href": "page/welcome-2.html",
            "icon": "fa fa-tachometer",
            "target": "_self"
        }
    ]
    userInfo = {"username": "admin", "role": "超级管理员", "avatar": "/static/images/0.jpg", "href": ""}

    init_data["homeInfo"] = homeInfo
    init_data["logoInfo"] = logoInfo
    init_data["menuInfo"] = menuInfo
    init_data["userInfo"] = userInfo
    return json.loads(json.dumps(init_data))
