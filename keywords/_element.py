# -*- coding: utf-8 -*-

from SongzAppiumLibrary.locators import ElementFinder
from keywordgroup import KeywordGroup
from robot.libraries.BuiltIn import BuiltIn
import ast
# added by songz
from robot.utils import timestr_to_secs
# added by songz

class _ElementKeywords(KeywordGroup):
    def __init__(self):
        self._element_finder = ElementFinder()
        self._bi = BuiltIn()

    # Public, element lookups
    def clear_text(self, locator):
        """Clears the text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self._info("Clear text field '%s'" % (locator))
        self._element_clear_text_by_locator(locator)

    def click_element(self, locator):
        """Click element identified by `locator`.

        Key attributes for arbitrary elements are `index` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Clicking element '%s'." % locator)
        self._element_find(locator, True, True).click()

    def click_button(self, index_or_name):
        """ Click button """
        _platform_class_dict = {'ios': 'UIAButton',
                                'android': 'android.widget.Button'}
        if self._is_support_platform(_platform_class_dict):
            class_name = self._get_class(_platform_class_dict)
            self._click_element_by_class_name(class_name, index_or_name)

    def input_text(self, locator, text):
        """Types the given `text` into text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self._info("Typing text '%s' into text field '%s'" % (text, locator))
        self._element_input_text_by_locator(locator, text)

    def input_password(self, locator, text):
        """Types the given password into text field identified by `locator`.

        Difference between this keyword and `Input Text` is that this keyword
        does not log the given password. See `introduction` for details about
        locating elements.
        """
        self._info("Typing password into text field '%s'" % locator)
        self._element_input_text_by_locator(locator, text)

    def input_value(self, locator, text):
        """Sets the given value into text field identified by `locator`. This is an IOS only keyword, input value makes use of set_value

        See `introduction` for details about locating elements.
        """
        self._info("Setting text '%s' into text field '%s'" % (text, locator))
        self._element_input_value_by_locator(locator, text)

    def hide_keyboard(self, key_name=None):
        """Hides the software keyboard on the device. (optional) In iOS, use `key_name` to press
        a particular key, ex. `Done`. In Android, no parameters are used.
        """
        driver = self._current_application()
        driver.hide_keyboard(key_name)

    def page_should_contain_text(self, text, loglevel='INFO'):
        """Verifies that current page contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        if text not in self.log_source(loglevel):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)

    def page_should_not_contain_text(self, text, loglevel='INFO'):
        """Verifies that current page not contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        if text in self.log_source(loglevel):
            self.log_source(loglevel)
            raise AssertionError("Page should not have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page does not contains text '%s'." % text)

    def page_should_contain_element(self, locator, loglevel='INFO'):
        """Verifies that current page contains `locator` element.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Givin
        """
        if not self._is_element_present(locator):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained element '%s' "
                                 "but did not" % locator)
        self._info("Current page contains element '%s'." % locator)

    def page_should_not_contain_element(self, locator, loglevel='INFO'):
        """Verifies that current page not contains `locator` element.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Givin
        """
        if self._is_element_present(locator):
            self.log_source(loglevel)
            raise AssertionError("Page should not have contained element '%s' "
                                 "but did not" % locator)
        self._info("Current page not contains element '%s'." % locator)

    def element_should_be_disabled(self, locator, loglevel='INFO'):
        """Verifies that element identified with locator is disabled.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.        
        """
        if self._element_find(locator, True, True).is_enabled():
            self.log_source(loglevel)
            raise AssertionError("Element '%s' should be disabled "
                                 "but did not" % locator)
        self._info("Element '%s' is disabled ." % locator)

    def element_should_be_enabled(self, locator, loglevel='INFO'):
        """Verifies that element identified with locator is enabled.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.        
        """
        if not self._element_find(locator, True, True).is_enabled():
            self.log_source(loglevel)
            raise AssertionError("Element '%s' should be enabled "
                                 "but did not" % locator)
        self._info("Element '%s' is enabled ." % locator)

    def element_name_should_be(self, locator, expected):
        element = self._element_find(locator, True, True)
        if expected != element.get_attribute('name'):
            raise AssertionError("Element '%s' name should be '%s' "
                                 "but it is '%s'." % (locator, expected, element.get_attribute('name')))
        self._info("Element '%s' name is '%s' " % (locator, expected))

    def element_value_should_be(self, locator, expected):
        element = self._element_find(locator, True, True)
        if expected != element.get_attribute('value'):
            raise AssertionError("Element '%s' value should be '%s' "
                                 "but it is '%s'." % (locator, expected, element.get_attribute('value')))
        self._info("Element '%s' value is '%s' " % (locator, expected))

    def element_attribute_should_match(self, locator, attr_name, match_pattern, regexp=False):
        """Verify that an attribute of an element matches the expected criteria.

        The element is identified by _locator_. See `introduction` for details
        about locating elements. If more than one element matches, the first element is selected.

        The _attr_name_ is the name of the attribute within the selected element.

        The _match_pattern_ is used for the matching, if the match_pattern is
        - boolean or 'True'/'true'/'False'/'false' String then a boolean match is applied
        - any other string is cause a string match

        The _regexp_ defines whether the string match is done using regular expressions (i.e. BuiltIn Library's
        [http://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Should%20Match%20Regexp|Should
        Match Regexp] or string pattern match (i.e. BuiltIn Library's
        [http://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Should%20Match|Should
        Match])


        Examples:

        | Element Attribute Should Match | xpath = //*[contains(@text,'foo')] | text | *foobar |
        | Element Attribute Should Match | xpath = //*[contains(@text,'foo')] | text | f.*ar | regexp = True |
        | Element Attribute Should Match | xpath = //*[contains(@text,'foo')] | enabled | True |

        | 1. is a string pattern match i.e. the 'text' attribute should end with the string 'foobar'
        | 2. is a regular expression match i.e. the regexp 'f.*ar' should be within the 'text' attribute
        | 3. is a boolead match i.e. the 'enabled' attribute should be True


        _*NOTE: *_
        On Android the supported attribute names are hard-coded in the
        [https://github.com/appium/appium/blob/master/lib/devices/android/bootstrap/src/io/appium/android/bootstrap/AndroidElement.java|AndroidElement]
        Class's getBoolAttribute() and getStringAttribute() methods.
        Currently supported (appium v1.4.11):
        _contentDescription, text, className, resourceId, enabled, checkable, checked, clickable, focusable, focused, longClickable, scrollable, selected, displayed_


        _*NOTE: *_
        Some attributes can be evaluated in two different ways e.g. these evaluate the same thing:

        | Element Attribute Should Match | xpath = //*[contains(@text,'example text')] | name | txt_field_name |
        | Element Name Should Be         | xpath = //*[contains(@text,'example text')] | txt_field_name |      |

        """
        elements = self._element_find(locator, False, True)
        if len(elements) > 1:
            self._info("CAUTION: '%s' matched %s elements - using the first element only" % (locator, len(elements)))

        attr_value = elements[0].get_attribute(attr_name)

        # ignore regexp argument if matching boolean
        if isinstance(match_pattern, bool) or match_pattern.lower() == 'true' or match_pattern.lower() == 'false':
            if isinstance(match_pattern, bool):
                match_b = match_pattern
            else:
                match_b = ast.literal_eval(match_pattern.title())

            if isinstance(attr_value, bool):
                attr_b = attr_value
            else:
                attr_b = ast.literal_eval(attr_value.title())

            self._bi.should_be_equal(match_b, attr_b)

        elif regexp:
            self._bi.should_match_regexp(attr_value,match_pattern,
                                        msg="Element '%s' attribute '%s' should have been '%s' "
                                        "but it was '%s'." % (locator, attr_name, match_pattern, attr_value),
                                        values=False)
        else:
            self._bi.should_match(attr_value,match_pattern,
                                        msg="Element '%s' attribute '%s' should have been '%s' "
                                        "but it was '%s'." % (locator, attr_name, match_pattern, attr_value),
                                        values=False)
        #if expected != elements[0].get_attribute(attr_name):
        #    raise AssertionError("Element '%s' attribute '%s' should have been '%s' "
        #                         "but it was '%s'." % (locator, attr_name, expected, element.get_attribute(attr_name)))
        self._info("Element '%s' attribute '%s' is '%s' " % (locator, attr_name, match_pattern))

    def get_elements(self, locator, first_element_only=False, fail_on_error=True):
        """Return elements that match the search criteria

        The element is identified by _locator_. See `introduction` for details
        about locating elements.

        If the _first_element_ is set to 'True' then only the first matching element is returned.

        If the _fail_on_error_ is set to 'True' this keyword fails if the search return nothing.

        Returns a list of [http://selenium-python.readthedocs.org/en/latest/api.html#module-selenium.webdriver.remote.webelement|WebElement] Objects.
        """
        return self._element_find(locator, first_element_only, fail_on_error)

    def get_element_attribute(self, locator, attribute):
        """Get element attribute using given attribute: name, value,...

        Examples:

        | Get Element Attribute | locator | name |
        | Get Element Attribute | locator | value |
        """
        elements = self._element_find(locator, False, True)
        ele_len = len(elements)
        if ele_len == 0:
            raise AssertionError("Element '%s' could not be found" % locator)
        elif ele_len > 1:
            self._info("CAUTION: '%s' matched %s elements - using the first element only" % (locator, len(elements)))

        try:
            attr_val = elements[0].get_attribute(attribute)
            self._info("Element '%s' attribute '%s' value '%s' " % (locator, attribute, attr_val))
            return attr_val
        except:
            raise AssertionError("Attribute '%s' is not valid for element '%s'" % (attribute, locator))

    def get_element_location(self, locator):
        """Get element location

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        element = self._element_find(locator, True, True)
        element_location = element.location
        self._info("Element '%s' location: %s " % (locator, element_location))
        return element_location

    def get_element_size(self, locator):
        """Get element size

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        element = self._element_find(locator, True, True)
        element_size = element.size
        self._info("Element '%s' size: %s " % (locator, element_size))
        return element_size




    # Private

    def _is_index(self, index_or_name):
        if index_or_name.startswith('index='):
            return True
        else:
            return False

    def _click_element_by_name(self, name):
        driver = self._current_application()
        try:
            element = driver.find_element_by_name(name)
        except Exception, e:
            raise Exception, e

        try:
            element.click()
        except Exception, e:
            raise Exception, 'Cannot click the element with name "%s"' % name

    def _find_elements_by_class_name(self, class_name):
        driver = self._current_application()
        elements = driver.find_elements_by_class_name(class_name)
        return elements

    def _find_element_by_class_name(self, class_name, index_or_name):
        elements = self._find_elements_by_class_name(class_name)

        if self._is_index(index_or_name):
            try:
                index = int(index_or_name.split('=')[-1])
                element = elements[index]
            except (IndexError, TypeError):
                raise Exception, 'Cannot find the element with index "%s"' % index_or_name
        else:
            found = False
            for element in elements:
                self._info("'%s'." % element.text)
                if element.text == index_or_name:
                    found = True
                    break
            if not found:
                raise Exception, 'Cannot find the element with name "%s"' % index_or_name

        return element

    def _get_class(self, platform_class_dict):
        return platform_class_dict.get(self._get_platform())

    def _is_support_platform(self, platform_class_dict):
        return platform_class_dict.has_key(self._get_platform())

    def _click_element_by_class_name(self, class_name, index_or_name):
        element = self._find_element_by_class_name(class_name, index_or_name)
        self._info("Clicking element '%s'." % element.text)
        try:
            element.click()
        except Exception, e:
            raise Exception, 'Cannot click the %s element "%s"' % (class_name, index_or_name)

    def _element_clear_text_by_locator(self, locator):
        try:
            element = self._element_find(locator, True, True)
            element.clear()
        except Exception, e:
            raise e

    def _element_input_text_by_locator(self, locator, text):
        try:
            element = self._element_find(locator, True, True)
            element.send_keys(text)
        except Exception, e:
            raise e

    def _element_input_text_by_class_name(self, class_name, index_or_name, text):
        try:
            element = self._find_element_by_class_name(class_name, index_or_name)
        except Exception, e:
            raise Exception, e

        self._info("input text in element as '%s'." % element.text)
        try:
            element.send_keys(text)
        except Exception, e:
            raise Exception, 'Cannot input text "%s" for the %s element "%s"' % (text, class_name, index_or_name)

    def _element_input_value_by_locator(self, locator, text):
        try:
            element = self._element_find(locator, True, True)
            element.set_value(text)
        except Exception, e:
            raise e

    def _element_find(self, locator, first_only, required, tag=None):
        application = self._current_application()
        elements = self._element_finder.find(application, locator, tag)
        if required and len(elements) == 0:
            raise ValueError("Element locator '" + locator + "' did not match any elements.")
        if first_only:
            if len(elements) == 0: return None
            return elements[0]
        return elements

    def _is_text_present(self, text):
        return text in self.get_source()

    def _is_element_present(self, locator):
        application = self._current_application()
        elements = self._element_finder.find(application, locator, None)
        return len(elements) > 0

    # added by songz
    def current_activity(self):
        """Current Activity

        Retrieves the current activity on the device.  -- added by songz
        """
        driver = self._current_application()
        activity = driver.current_activity
        self._info("current activity is '%s'." % activity)
        return activity

    def wait_activity(self, activity, timeout, interval=1):
        """Wait for an activity: block until target activity presents
        or time out.

        This is an Android-only method.  -- added by songz

        :Agrs:
         - activity - target activity
         - timeout - max wait time, in seconds
         - interval - sleep interval between retries, in seconds
        """
        timeout_seconds = timestr_to_secs(timeout)
        # Python hangs with negative values
        if timeout_seconds < 0:
            timeout_seconds = 0
        driver = self._current_application()
        result = driver.wait_activity(activity, float(timeout_seconds), interval)
        self._info("wait activity to enter.")
        return result

    def start_activity(self, app_package, app_activity, **opts):
        """Opens an arbitrary activity during a test. If the activity belongs to
        another application, that application is started and the activity is opened.

        This is an Android-only method.    -- added by songz

        :Args:
        - app_package - The package containing the activity to start.
        - app_activity - The activity to start.
        - app_wait_package - Begin automation after this package starts (optional).
        - app_wait_activity - Begin automation after this activity starts (optional).
        - intent_action - Intent to start (optional).
        - intent_category - Intent category to start (optional).
        - intent_flags - Flags to send to the intent (optional).
        - optional_intent_arguments - Optional arguments to the intent (optional).
        - stop_app_on_reset - Should the app be stopped on reset (optional)?
        """
        driver = self._current_application()
        driver.start_activity(app_package, app_activity, **opts)
        self._info("start the target activity.")

    def open_notifications(self):
        """Open notification shade in Android (API Level 18 and above)    -- added by songz
        """
        driver = self._current_application()
        driver.open_notifications()
        self._info("open the notification bar.")

    def available_ime_engines(self):
        """Get the available input methods for an Android device. Package and
        activity are returned (e.g., ['com.android.inputmethod.latin/.LatinIME'])    -- added by songz

        Android only.
        """
        driver = self._current_application()
        available_ime_engines = driver.available_ime_engines
        self._info("the available input methods is:  '%s'." % available_ime_engines)
        return available_ime_engines

    def is_ime_active(self):
        """Checks whether the device has IME service active. Returns True/False.    -- added by songz

        Android only.
        """
        driver = self._current_application()
        is_ime_active = driver.is_ime_active()
        self._info("is the device has IME service active:  '%s'." % is_ime_active)
        return is_ime_active

    def activate_ime_engine(self, engine):
        """Activates the given IME engine on the device.

        Android only.

        :Args:
         - engine - the package and activity of the IME engine to activate (e.g.,
            'com.android.inputmethod.latin/.LatinIME')        -- added by songz
        """
        driver = self._current_application()
        driver.activate_ime_engine(engine)
        self._info("activate the given IME engine on the device.")

    def deactivate_ime_engine(self):
        """Deactivates the currently active IME engine on the device.    -- added by songz

        Android only.
        """
        driver = self._current_application()
        driver.deactivate_ime_engine()
        self._info("deactivate the given IME engine on the device.")

    def get_text(self, element):
        """Returns the text of the element.    -- added by songz
        """
        self._info("get the text of the element.")
        return element.text

    def get_size(self, element):
        """Returns the size of the element.    -- added by songz
        """
        self._info("get the size of the element.")
        return element.size

    def get_location(self, element):
        """Returns the location of the element.    -- added by songz
        """
        self._info("get the location of the element.")
        return element.location

    def select_element(self, elements, index):
        """Return the value of inputted index of elements list.

           the format of elements list must be ${els}: a variable, not a list variable  - added by songz
        """
        element = elements[int(index)]
        return element

    def click_element_after_find_it(self,locator):
        """Foreach the identifies, and click the text-matched element identified by `locator`.

        Key attributes for arbitrary elements are `index` and `name`. See
        `introduction` for details about locating elements.    - added by songz
        """
        driver = self._current_application()
        size = driver.get_window_size()
        width = int(size['width'])
        height = int(size['height'])
        self._info("Clicking element after find it: '%s'." % locator)

        isFinded = False
        while not isFinded:
            try:
                element = self._element_find(locator,True,True)
                element.click()
                isFinded = True
            except:
                driver.swipe(width/2, height*7/8, width/2, 1)
                self._info("Swipe to the end of the page.")
                isFinded = False

    def click_by_element_given(self, element):
        """Click element by element given.

           :argument element    - added by songz
        """
        self._info("click by element given.")
        element.click()

    def get_element(self, locator, first_element_only=True, fail_on_error=True):
        """Return element that match the search criteria.

        Returns webelement Object.   - added by songz
        """
        return self._element_find(locator, first_element_only, fail_on_error)




