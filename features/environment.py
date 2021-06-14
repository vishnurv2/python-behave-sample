from selenium import webdriver

import os, json

CONFIG_FILE = os.environ['CONFIG_FILE'] if 'CONFIG_FILE' in os.environ else 'config/single.json'
TASK_ID = int(os.environ['TASK_ID']) if 'TASK_ID' in os.environ else 0

with open(CONFIG_FILE) as data_file:
    CONFIG = json.load(data_file)


LT_USERNAME = os.environ['LT_USERNAME'] if 'LT_USERNAME' in os.environ else CONFIG['user']
LT_ACCESS_KEY = os.environ['LT_ACCESS_KEY'] if 'LT_ACCESS_KEY' in os.environ else CONFIG['key']


def before_feature(context, feature):
    desired_capabilities = CONFIG['environments'][TASK_ID]

    for key in CONFIG["capabilities"]:
        if key not in desired_capabilities:
            desired_capabilities[key] = CONFIG["capabilities"][key]


    context.browser = webdriver.Remote(
        desired_capabilities=desired_capabilities,
        command_executor="http://%s:%s@hub.lambdatest.com/wd/hub" % (LT_USERNAME, LT_ACCESS_KEY)
    )

def after_feature(context, feature):
    context.browser.quit()
