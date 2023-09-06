from flask import Blueprint, render_template

import com.loadconf

SettingPage = Blueprint('setting', __name__, )


@SettingPage.route("/setting/page", methods=["GET"])
def page():
    setting = com.loadconf.Config
    project_list = com.loadconf.load_project_list(com.loadconf.ConfigPath)
    return render_template('/setting.html',setting = setting,project_list= project_list)
