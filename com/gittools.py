#!/usr/bin/python3
# -- coding: utf-8 --**
import os
import pathlib
import subprocess
import time

from com.gitlab_api import GitlabApi
from com.loadconf import Config
from com.logger import logger


def nowsync(project):
    logger.info("开始同步 %s" % project)
    repo_path = Config.repo_base_path + project.replace("/", "_").replace("-", "_")
    if not os.path.exists(repo_path):
        pid = GitlabApi.CreateGroupByLongPath(os.path.dirname(project))
        if pid <= 0:
            logger.error("创建group失败")
            return
        clone_cmd = make_clone_cmd(project, repo_path)
        # 在缓存目录执行clone命令
        code, msg = cmd(clone_cmd, Config.repo_base_path)
        if code != 0:
            logger.error("%s 失败: %s %s" % (project, clone_cmd, msg))
            return
        else:
            logger.info("%s 执行完毕", clone_cmd)
        time.sleep(3)
        # clone命令需要添加一个cz的remote 后续使用这个命令push
        add_remote_cmd = make_add_remote_cmd(project, repo_path)
        code, msg = cmd(add_remote_cmd, repo_path)
        if code != 0:
            logger.error("%s 失败: %s %s" % (project, add_remote_cmd, msg))
            return
        else:
            logger.info("%s 执行成功" % add_remote_cmd)
    # 指定fetch命令
    fetch_cmd = make_fetch_cmd()
    code, msg = cmd(fetch_cmd, repo_path)
    if code != 0:
        logger.error("%s 失败: %s %s" % (project, fetch_cmd, msg))
        return
    else:
        logger.info("%s 执行成功" % fetch_cmd)
    # 执行push功能
    push_cmd = make_push_cmd()
    code, msg = cmd(push_cmd, repo_path)
    if code != 0:
        logger.error("%s 失败: %s %s" % (project, push_cmd, msg))
        return
    else:
        logger.info("%s 执行成功" % push_cmd)


def make_fetch_cmd():
    return "git fetch origin"


def make_push_cmd():
    return "git push -f cz --tags 'refs/remotes/origin/*:refs/heads/*'"


def make_add_remote_cmd(project, repo_path):
    return "git remote add cz %s://oauth2:%s@%s/%s.git" % (
        Config.target_protocol, Config.target_token, Config.target_domain, project)


def make_clone_cmd(project, repo_path):
    return "git clone %s://oauth2:%s@%s/%s.git  %s" % (
        Config.source_protocol, Config.source_token, Config.source_domain, project, repo_path)


def cmd(cmd_str, work_dir):
    p = subprocess.Popen(cmd_str, shell=True, cwd=work_dir, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return p.returncode, stderr.decode("utf-8") + stdout.decode("utf-8")
    return p.returncode, stderr.decode("utf-8") + stdout.decode("utf-8")


def lock(work_dir):
    work_dir = work_dir.replace("/", "_")
    path = pathlib.Path("%s/%s.lock" % (Config.lock_path, work_dir))
    if path.exists():
        logger.info("等待任务完成:%s" % work_dir)
        return True
    try:
        path.touch()
    except Exception as e:
        logger.error("锁定文件创建:%s" % e)
    return False


def unlock(work_dir):
    work_dir = work_dir.replace("/", "_")
    path = pathlib.Path("%s/%s.lock" % (Config.lock_path, work_dir))
    if path.exists():
        path.unlink()
