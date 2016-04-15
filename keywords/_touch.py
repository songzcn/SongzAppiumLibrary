# -*- coding: utf-8 -*-

from appium.webdriver.common.touch_action import TouchAction
from SongzAppiumLibrary.locators import ElementFinder
from keywordgroup import KeywordGroup


class _TouchKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()

    # Public, element lookups
    def zoom(self, locator, percent="200%", steps=1):
        """
        Zooms in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.zoom(element=element, percent=percent, steps=steps)

    def pinch(self, locator, percent="200%", steps=1):
        """
        Pinch in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.pinch(element=element, percent=percent, steps=steps)

    def swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        """
        Swipe from one point to another point, for an optional duration.
        """
        driver = self._current_application()
        driver.swipe(start_x, start_y, end_x, end_y, duration)

    def scroll(self, start_locator, end_locator):
        """
        Scrolls from one element to another
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        el1 = self._element_find(start_locator, True, True)
        el2 = self._element_find(end_locator, True, True)
        driver = self._current_application()
        driver.scroll(el1, el2)
        
    def scroll_to(self, locator):
        """Scrolls to element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scrollTo", {"element": element.id})
        
    # def long_press(self, locator):
    #     """ Long press the element """
    #     driver = self._current_application()
    #     element = self._element_find(locator, True, True)
    #     long_press = TouchAction(driver).long_press(element)
    #     long_press.perform()

    def long_click(self, locator, dur):
        """ Long press the element
        :Args:
        locator, duration(ms)           - added by songz
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        long_press = TouchAction(driver).long_press(el=element, x=None, y=None, duration=dur)
        long_press.perform()

    def tap(self, locator):
        """ Tap on element """
        driver = self._current_application()
        el = self._element_find(locator, True, True)
        action = TouchAction(driver)
        action.tap(el).perform()
        
    def click_a_point(self, x=0, y=0):
        """ Click on a point"""
        self._info("Clicking on a point (%s,%s)." % (x,y))
        driver = self._current_application()
        action = TouchAction(driver)
        try:
            action.press(x=float(x), y=float(y)).perform()
        except:
            assert False, "Can't click on a point at (%s,%s)" % (x,y)

    def swipe_percentage(self,p1,p2,p3,p4,duration=1000):
        """
        Swipe from one point to another point by percentage, for an optional duration.
        :argument percentage like 0.5,0.27 is ok     - added by songz
        """
        driver = self._current_application()
        size = driver.get_window_size()
        width = int(size['width'])
        height = int(size['height'])
        driver.swipe(width*float(p1),height*float(p2),width*float(p3),height*float(p4),duration)

    def swipe_element_percentage(self,element,p1,p2,p3,p4,duration=1000):
        """
        Swipe from one point to another point in selected element by percentage, for an optional duration.
        :argument percentage like 0.5,0.27 is ok     - added by songz
        """
        driver = self._current_application()
        loc = element.location
        sz = element.size
        locx = int(loc['x'])
        locy = int(loc['y'])
        width = int(sz['width'])
        height = int(sz['height'])
        x1 = locx + width*float(p1)
        y1 = locy + height*float(p2)
        x2 = locx + width*float(p3)
        y2 = locy + height*float(p4)
        driver.swipe(x1,y1,x2,y2,duration)
