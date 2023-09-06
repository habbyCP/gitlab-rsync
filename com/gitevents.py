#!/usr/bin/python3
# -- coding: utf-8 --**


from com.gittools import nowsync, lock, unlock
from com.logger import logger
from com.loadconf import  load_project_list, ConfigPath


def event_deal(message):
    logger.info('接收到新事件')
    project = ""
    if isinstance(message, dict):
        if not allow_action(message):
            return
        if allow_project(message["project"]["path_with_namespace"], load_project_list(ConfigPath)):
            project = message["project"]["path_with_namespace"]
            logger.info("获取到新任务:" + message["project"]["path_with_namespace"])
        else:
            logger.warn(message["project"]["path_with_namespace"] + " 不在白名单")
    else:
        logger.info('接收' + str(type(message)) + '类型message,无处理程序~')

    if len(project) > 0:
        # 加锁，如果已经锁定则返回
        if lock(project):
            return
        try:
            nowsync(project)
        except Exception as e:
            logger.error('事件处理失败' + str(e))
        finally:
            # 最后都会解锁的
            unlock(project)
            logger.info('事件处理完成')


def allow_action(message):
    if 'event_name' not in message.keys() or "project" not in message.keys():
        logger.error("webhook参数缺乏 event_name project；原始内容：%s" % message)
        return False
    if message['event_name']  not in ["tag_push","repository_update","push"]:
        logger.info('不受支持的事件 %s', message['event_name'])
        return False
    return True


def allow_project(project, project_list):
    for s in project_list:
        if project.find(s) == 0:
            return True
    return False
