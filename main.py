import uiautomator2 as u2
from uiautomator2 import Direction
import os

# Client:python script
# Server:atx-agent running on the Android device
d = u2.connect("R52RA0C2MFF")
d2 = u2.connect("R5CW21J3P5A")
# d.healthcheck()
# d2.healthcheck()


def pairScreenshot():

    # Directory for saving files
    base_dir = r'C:\Users\xijia\OneDrive\Desktop'
    pkg_name = 'com.samsung.android.calendar'
    save_dir = os.path.join(base_dir, pkg_name)

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    # `<pair_id>_<device_type>_<activiey_name>.<file_type>
    phone_image_path = os.path.join(save_dir, 'timeStamp1_phone_TopLevelActivity.png')
    phone_xml_path = os.path.join(save_dir, 'timeStamp1_phone_TopLevelActivity.xml')
    tablet_image_path = os.path.join(save_dir, 'timeStamp1_table_TopLevelActivity.png')
    tablet_xml_path = os.path.join(save_dir, 'timeStamp1_tablet_TopLevelActivity.xml')

    # screenshot and save
    image = d.screenshot()
    image2 = d2.screenshot()
    xml = d.dump_hierarchy()
    xml2 = d2.dump_hierarchy()

    image.save(phone_image_path)
    with open(phone_xml_path, 'w') as file:
        file.write(xml)
    image2.save(tablet_image_path)
    with open(tablet_xml_path, 'w') as file:
        file.write(xml2)


""" Basic Settings """


def waitTime():  # normally default or change: if not show in.s, UiObjectNotFoundError will raise
    # Global
    d.set_new_command_timeout(300)
    # Implicit wait: Set default element wait time, unit seconds
    d.implicitly_wait(10.0)
    # local: click/set_text/clear_text...(timeout=...)
    # time.sleep()
    d.wait_activity('com.sec.android.app.clockpackage', timeout=10)


""" App management """


def appBasic():
    """ deprecated method session
    session--environment (context for the automation script to interact with the app)
    Initializing a state of interaction
    d.app_start/stop("package_name"): straightforward commands
    """
    # d.app_start('com.sec.android.app.clockpackage')
    # d.session('com.sec.android.app.clockpackage')


def pushPullFile():
    # src:source file, dst:destination file
    # Internal storage: completely private to the application
    # /sdcard/ - primary external storage in a consistent way across different devices
    # Android users to refer to the user-accessible external storage
    # one issue: the permission denied ls data ###
    d.push("demo.txt", "/sdcard/")
    d.pull("/sdcard/demo.txt", r'C:\Users\xijia\OneDrive\Desktop\pullDemo.txt')


""" UI Automation """


def shellCommand():
    """blocking command"""
    # output, exit_code = d.shell("pwd", timeout=60)  # timeout 60s (Default)
    output, exit_code = d.shell(["ls", "-l"])
    print(output, exit_code)  # root: /

    """long-running without blocking--iterate over the output line by line as it comes in"""
    # add stream=True will return requests.models.Response object.
    # close() to stop


def infoBasic():
    print(d.info)
    print(d2.info)
    # print(d.device_info)
    # # return the tuple (width, height); represent the screen resolution in pixels
    # print(d.window_size())
    # Get Widget center point:
    # x, y = d(text="Spotify").center()  # = offset=(0.5, 0.5)
    # # .click(offset=(0, 0)): top-left corner of the element
    # print(x, y)  # Actual click coordinates:
    # Adding the offset-scaled width and height to the top-left corner coordinates


def keyEvent():
    d.screen_on()  # d.screen_off()
    print(d.info.get('screenOn'))  # True or False
    # d.unlock() ???????? - but it can use to activate the screen...


def screenshot():
    """directly saves the screenshot to a file named ".jpg/.png format" on the computer"""
    d.screenshot("home.jpg")  # with parameter
    image = d.screenshot()  # if no parameter: default format="pillow"
    image.save("home2.jpg")
    # get PIL.Image object/images --useful: manipulate the image using PIL (Python Imaging Library) before saving it.
    # parameter: 2-tuple (width, height) size in pixels
    image.resize((200, 400))
    """get opencv formatted images."""
    import cv2
    image = d.screenshot(format='opencv')
    cv2.imwrite('homeF.jpg', image)
    """get raw binary jpeg data"""
    imagebin = d.screenshot(format='raw')
    open("some.jpg", "wb").write(imagebin)


def selector():
    """click_exists vs click
    .click--Assumes that the element is already present and visible on the screen
    .click_exists -- when dealing with elements
    that might take some time to appear due to loading or other delays.
        checks if the element exists and
        is visible on the screen within a specified timeout period
            If the element becomes visible: click
            If not: not click -> return false
    """
    d(text="Spotify").click()
    d(text="Spotify").click_exists(timeout=10.0)
    # click until element gone, return bool
    d(text="Spotify").click_gone(maxretry=10, interval=1.0)

    d(resourceId="com.sec.android.app.launcher:id/icon", text="Clock").click()
    # Multiple instances (root UI hierarchy)
    # instance is not equal to the index
    d(resourceId="com.sec.android.app.launcher:id/icon", instance=4).click()
    # UI hierarchy children by text or description or instance
    # d(resourceIdParent).child(resourceIdChild) /child_by_text()
    d(resourceId="com.sec.android.app.launcher:id/hotseat_layout").child(  # socialFolder
        resourceId="com.sec.android.app.launcher:id/folder_icon_view").click()
    # .sibling(e.g. className=''...) if only one sibling do not need the parameter

    # relative positioning methods to get the view
    d(resourceId="com.sec.android.app.launcher:id/icon", text="Clock").right().click()
    # position or percentage
    d.click(689, 1611)
    d.click(0.641, 0.687)


def gestureInteraction():
    """Swipe(quicker, flinging motions) vs Drag(more controlled gesture)"""
    # SwipeExt
    d.swipe_ext("left", scale=0.9)
    # 从左往右，出现左侧的页面
    d.swipe_ext(Direction.HORIZ_BACKWARD)
    d(text="Settings").swipe("left", steps=10)
    # Drag: I object to a screen point (x, y)
    # in 0.5 second->then return true
    d(text="Spotify").drag_to(928, 1009, duration=0.5)
    # step--duration and granularity of the swipe motion
    d(text="Spotify").swipe("up", steps=20)


def inputMethod():
    # I: selector - method
    d(resourceId="com.youdao.dict:id/et_search_enter").send_keys("element")
    (d.xpath(
        '//*[@resource-id="com.google.android.inputmethod.latin:id/key_pos_ime_action"]/'
        'android.widget.FrameLayout[1]/android.widget.ImageView[1]')
     .click())  # or method two
    d.clear_text()
    # II: 模拟输入法 github
    d.set_fastinput_ime(True)  # false -- 切换成正常的输入法
    d.send_action("search")


def imageMatch():
    image = "home2.jpg"
    print(d.image.match(image))

# waitTime()
# appBasic()
# pushPullFile()

# shellCommand()
# infoBasic()
# screenshot()
# selector()
# gestureInteraction()
# inputMethod()


# R52RA0C2MFF     device-Tablet
# R5CW21J3P5A     device-Android phone

# 'dinnerdeal.android.customer'
# 'com.sec.android.app.clockpackage'
# d.healthcheck()
# imageMatch()
# pairScreenshot()