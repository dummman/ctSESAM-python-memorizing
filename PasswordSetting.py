#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Sets of password settings for a domain.
"""

from datetime import datetime
import getpass
import string
from base64 import b64encode, b64decode

DEFAULT_SALT = "pepper".encode('utf-8')
DEFAULT_CHARACTER_SET_LOWER_CASE = "abcdefghijklmnopqrstuvwxyz"
DEFAULT_CHARACTER_SET_UPPER_CASE = "ABCDEFGHJKLMNPQRTUVWXYZ"
DEFAULT_CHARACTER_SET_DIGITS = string.digits
DEFAULT_CHARACTER_SET_EXTRA = '#!"§$%&/()[]{}=-_+*<>;:.'


class PasswordSetting:
    """
    This saves one set of settings for a certain domain. Use a PasswordSettingsManager to save the settings to a file.
    """
    def __init__(self, domain):
        self.domain = domain
        self.url = None
        self.username = None
        self.legacy_password = None
        self.notes = None
        self.iterations = 4096
        self.salt = DEFAULT_SALT
        self.length = 10
        self.creation_date = datetime.now()
        self.modification_date = self.creation_date
        self.used_characters = self.get_default_character_set()
        self.reserved = None
        self.synced = False

    def get_domain(self):
        """
        Returns the domain name or another string used in the domain field.

        :return: the domain
        :rtype: str
        """
        return self.domain

    def set_domain(self, domain):
        """
        Change the domain string.

        :param domain: the domain
        :type domain: str
        """
        self.domain = domain
        self.synced = False

    def has_username(self):
        """
        Returns True if the username is set.

        :return:
        :rtype: bool
        """
        return self.username and len(str(self.username)) > 0

    def get_username(self):
        """
        Returns the username or an empty string if there was no username.

        :return: the username
        :rtype: str
        """
        if self.username:
            return self.username
        else:
            return ""

    def set_username(self, username):
        """
        Set the username.

        :param username: the username
        :type username: str
        """
        if username != self.username:
            self.synced = False
        self.username = username

    def has_legacy_password(self):
        """
        Returns True if the legacy password is set.

        :return:
        :rtype: bool
        """
        return self.legacy_password and len(str(self.legacy_password)) > 0

    def get_legacy_password(self):
        """
        Returns the legacy password if set or an empty string otherwise.

        :return: the legacy password
        :rtype: str
        """
        if self.legacy_password:
            return self.legacy_password
        else:
            return ""

    def set_legacy_password(self, legacy_password):
        """
        Set a legacy password.

        :param legacy_password: a legacy password
        :type legacy_password: str
        """
        if legacy_password != self.legacy_password:
            self.synced = False
        self.legacy_password = legacy_password

    def use_letters(self):
        """
        Returns true if the character set contains the default set of letters at the default position and with the
        default order.

        :return: does it use letters?
        :rtype: bool
        """
        return self.used_characters[:len(DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE)] == \
            DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE

    def set_use_letters(self, use_letters):
        """
        If set to True the letters are moved to the default position and brought into the default order. Missing
        letters are inserted. If set to False all default letters are removed from the character set.

        :param use_letters:
        :type use_letters: bool
        """
        old_character_set = self.used_characters
        pos = 0
        while pos < len(self.used_characters):
            if self.used_characters[pos] in DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE:
                self.used_characters = self.used_characters[:pos] + self.used_characters[pos + 1:]
            else:
                pos += 1
        if use_letters:
            self.used_characters = DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE + \
                self.used_characters
        if old_character_set != self.used_characters:
            self.synced = False

    def use_lower_case(self):
        """
        Returns true if the character set contains the default set of lower case letters at the default position and
        with the default order.

        :return: using lower case?
        :rtype: bool
        """
        return self.used_characters[:len(DEFAULT_CHARACTER_SET_LOWER_CASE)] == DEFAULT_CHARACTER_SET_LOWER_CASE

    def set_use_lower_case(self, use_lower_case):
        """
        If set to True the lower case letters are moved to the default position and brought into the default order.
        Missing lower case letters are inserted. If set to False all lower case letters are removed from the character
        set.

        :param use_lower_case:
        :type use_lower_case: bool
        """
        old_character_set = self.used_characters
        pos = 0
        while pos < len(self.used_characters):
            if self.used_characters[pos] in DEFAULT_CHARACTER_SET_LOWER_CASE:
                self.used_characters = self.used_characters[:pos] + self.used_characters[pos + 1:]
            else:
                pos += 1
        if use_lower_case:
            self.used_characters = DEFAULT_CHARACTER_SET_LOWER_CASE + self.used_characters
        if old_character_set != self.used_characters:
            self.synced = False

    def use_upper_case(self):
        """
        Returns true if the character set contains the default set of upper case letters at the default position and
        with the default order.

        :return: use upper case?
        :rtype: bool
        """
        return self.used_characters[
            len(DEFAULT_CHARACTER_SET_LOWER_CASE):len(
                DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE)] \
            == DEFAULT_CHARACTER_SET_UPPER_CASE

    def set_use_upper_case(self, use_upper_case):
        """
        If set to True the upper case letters are moved to the default position and brought into the default order.
        Missing upper case letters from the default set of upper case letters are inserted. If set to False all
        default upper case letters are removed from the character set.

        :param use_upper_case:
        :type use_upper_case: bool
        """
        old_character_set = self.used_characters
        pos = 0
        while pos < len(self.used_characters):
            if self.used_characters[pos] in DEFAULT_CHARACTER_SET_UPPER_CASE:
                self.used_characters = self.used_characters[:pos] + self.used_characters[pos + 1:]
            else:
                pos += 1
        if use_upper_case:
            self.used_characters = self.used_characters[:len(DEFAULT_CHARACTER_SET_LOWER_CASE)] + \
                DEFAULT_CHARACTER_SET_LOWER_CASE + self.used_characters[len(DEFAULT_CHARACTER_SET_LOWER_CASE):]
        if old_character_set != self.used_characters:
            self.synced = False

    def use_digits(self):
        """
        Returns true if the character set contains digits at the default position and with the default order.

        :return: use digits?
        :rtype: bool
        """
        return self.used_characters[
            len(DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE):len(
                DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE + DEFAULT_CHARACTER_SET_DIGITS)] \
            == DEFAULT_CHARACTER_SET_DIGITS

    def set_use_digits(self, use_digits):
        """
        If set to True the digits are moved to the default position and brought into the default order.
        Missing digits are inserted. If set to False all digits are removed from the character set.

        :param use_digits:
        :type use_digits: bool
        """
        old_character_set = self.used_characters
        pos = 0
        while pos < len(self.used_characters):
            if self.used_characters[pos] in DEFAULT_CHARACTER_SET_DIGITS:
                self.used_characters = self.used_characters[:pos] + self.used_characters[pos + 1:]
            else:
                pos += 1
        if use_digits:
            self.used_characters = self.used_characters[
                :len(DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE)] + \
                DEFAULT_CHARACTER_SET_DIGITS + self.used_characters[
                    len(DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE):]
        if old_character_set != self.used_characters:
            self.synced = False

    def use_extra(self):
        """
        Returns true if the character set contains the special characters from the default set at the default position
        and with the default order.

        :return: use special characters?
        :rtype: bool
        """
        return self.used_characters[
            len(DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE + DEFAULT_CHARACTER_SET_DIGITS):] \
            == DEFAULT_CHARACTER_SET_EXTRA

    def set_use_extra(self, use_extra):
        """
        If set to True the default special characters are moved to the default position and brought into the default
        order. Missing special characters from the default set are inserted. If set to False all special characters
        from the default set are removed from the character set.

        :param use_extra:
        :type use_extra: bool
        """
        old_character_set = self.used_characters
        pos = 0
        while pos < len(self.used_characters):
            if self.used_characters[pos] in DEFAULT_CHARACTER_SET_EXTRA:
                self.used_characters = self.used_characters[:pos] + self.used_characters[pos + 1:]
            else:
                pos += 1
        if use_extra:
            self.used_characters += DEFAULT_CHARACTER_SET_EXTRA
        if old_character_set != self.used_characters:
            self.synced = False

    def use_custom_character_set(self):
        """
        Returns false if the character set is set to the default character set.

        :return: are we using a custom character set?
        :rtype: bool
        """
        return not self.used_characters == DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE + \
            DEFAULT_CHARACTER_SET_DIGITS + DEFAULT_CHARACTER_SET_EXTRA

    @staticmethod
    def get_default_character_set():
        """
        Returns the default character set. This is completely independent of the character set stored at instances
        of this class.

        :return: the default character set
        :rtype: str
        """
        return DEFAULT_CHARACTER_SET_LOWER_CASE + DEFAULT_CHARACTER_SET_UPPER_CASE + \
            DEFAULT_CHARACTER_SET_DIGITS + DEFAULT_CHARACTER_SET_EXTRA

    def get_character_set(self):
        """
        Returns the character set as a string.

        :return: character set
        :rtype: str
        """
        return self.used_characters

    def set_custom_character_set(self, character_set):
        """
        Sets the character set to the given string. Use this method to save reordered default sets.

        :param str character_set: character set
        """
        if self.used_characters != character_set:
            self.synced = False
        self.used_characters = character_set

    def get_salt(self):
        """
        Returns the salt.

        :return: the salt
        :rtype: bytes
        """
        return self.salt

    @staticmethod
    def get_default_salt():
        """
        This returns the default salt. This is completely independent of the salt stored at instances
        of this class.

        :return: the default salt
        :rtype: bytes
        """
        return DEFAULT_SALT

    def set_salt(self, salt):
        """
        You should normally pass bytes as a salt. For convenience this method also accepts strings which get
        UTF-8 encoded and stored in binary format. If in doubt pass bytes.

        :param salt:
        :type salt: bytes or str
        """
        if type(salt) == bytes:
            if self.salt != salt:
                self.synced = False
            self.salt = salt
        elif type(salt) == str:
            if self.salt != salt.encode('utf-8'):
                self.synced = False
            self.salt = salt.encode('utf-8')
        else:
            raise TypeError("The salt should be bytes.")

    def get_length(self):
        """
        Returns the desired password length.

        :return: length
        :rtype: int
        """
        return self.length

    def set_length(self, length):
        """
        Sets the desired length.

        :param length:
        :type length: int
        """
        if self.length != length:
            self.synced = False
        self.length = length

    def get_iterations(self):
        """
        Returns the iteration count which is to be used.

        :return: iteration count
        :rtype: int
        """
        return self.iterations

    def set_iterations(self, iterations):
        """
        Sets the iteration count integer.

        :param iterations:
        :type iterations: int
        """
        if self.iterations != iterations:
            self.synced = False
        self.iterations = iterations

    def get_c_date(self):
        """
        Returns the creation date as a datetime object.

        :return: the creation date
        :rtype: datetime
        """
        return self.creation_date

    def get_creation_date(self):
        """
        Returns the creation date as string.

        :return: the creation date
        :rtype: str
        """
        return self.creation_date.strftime("%Y-%m-%dT%H:%M:%S")

    def set_creation_date(self, creation_date):
        """
        Sets the creation date passed as string.

        :param creation_date:
        :type creation_date: str
        """
        if self.creation_date != creation_date:
            self.synced = False
        try:
            self.creation_date = datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            print("This date has a wrong format: " + creation_date)
            self.creation_date = datetime.now()
        if self.modification_date < self.creation_date:
            self.modification_date = self.creation_date

    def get_m_date(self):
        """
        Returns the modification date as a datetime object.

        :return: the modification date
        :rtype: datetime
        """
        return self.modification_date

    def get_modification_date(self):
        """
        Returns the modification date as string.

        :return: the modification date
        :rtype: str
        """
        return self.modification_date.strftime("%Y-%m-%dT%H:%M:%S")

    def set_modification_date(self, modification_date=None):
        """
        Sets the modification date passed as string.

        :param modification_date:
        :type modification_date: str
        """
        if modification_date and self.modification_date != modification_date:
            self.synced = False
        if type(modification_date) == str:
            try:
                self.modification_date = datetime.strptime(modification_date, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                print("This date has a wrong format: " + modification_date)
                self.modification_date = datetime.now()
        else:
            self.modification_date = datetime.now()
        if self.modification_date < self.creation_date:
            print("The modification date was before the creation Date. " +
                  "Setting the creation date to the earlier date.")
            self.creation_date = self.modification_date

    def get_notes(self):
        """
        Returns the notes.

        :return: the notes
        :rtype: str
        """
        if self.notes:
            return self.notes
        else:
            return ""

    def set_notes(self, notes):
        """
        Sets some note. This overwrites existing notes.

        :param notes:
        :type notes: str
        """
        if notes != self.notes:
            self.synced = False
        self.notes = notes

    def get_url(self):
        """
        Returns a url if there is one.

        :return: the url
        :rtype: str
        """
        if self.url:
            return self.url
        else:
            return ""

    def set_url(self, url):
        """
        Sets a url.

        :param url: the url
        :type url: str
        """
        if url != self.url:
            self.synced = False
        else:
            return self.url

    def get_reserved(self):
        """
        Returns the 'reserved' field

        :return: reserved
        :rtype: str
        """
        if self.reserved:
            return self.reserved
        else:
            return ""

    def set_reserved(self, reserved):
        """
        Sets the 'reserved' field

        :param reserved: the content of the 'reserved' field
        :type reserved: str
        """
        if reserved != self.reserved:
            self.synced = False
        else:
            return self.reserved

    def is_synced(self):
        """
        Query if the synced flag is set. The flag switches to false if settings are changed.

        :return: is synced?
        :rtype: bool
        """
        return self.synced

    def set_synced(self, is_synced=True):
        """
        Sets the synced state. Call this after syncing.

        :param is_synced:
        :type is_synced: bool
        """
        self.synced = is_synced

    def to_dict(self):
        """
        Returns a dictionary with settings to be saved.

        :return: a dictionary with settings to be saved
        :rtype: dict
        """
        domain_object = {"domain": self.get_domain()}
        if self.get_url():
            domain_object["url"] = self.get_url()
        if self.get_username():
            domain_object["username"] = self.get_username()
        if self.get_legacy_password():
            domain_object["legacyPassword"] = self.get_legacy_password()
        if self.notes:
            domain_object["notes"] = self.get_notes()
        domain_object["iterations"] = self.get_iterations()
        if self.salt:
            domain_object["salt"] = str(b64encode(self.get_salt()), encoding='utf-8')
        domain_object["length"] = self.get_length()
        domain_object["cDate"] = self.get_creation_date()
        domain_object["mDate"] = self.get_modification_date()
        domain_object["usedCharacters"] = self.get_character_set()
        if self.get_reserved():
            domain_object["reserved"] = self.get_reserved()
        return domain_object

    def load_from_dict(self, loaded_setting):
        """
        Loads the setting from a dictionary.

        :param loaded_setting:
        :type loaded_setting: dict
        """
        if "url" in loaded_setting:
            self.set_url(loaded_setting["url"])
        if "username" in loaded_setting:
            self.set_username(loaded_setting["username"])
        if "legacyPassword" in loaded_setting:
            self.set_legacy_password(loaded_setting["legacyPassword"])
        if "notes" in loaded_setting:
            self.set_notes(loaded_setting["notes"])
        if "iterations" in loaded_setting:
            self.set_iterations(loaded_setting["iterations"])
        if "salt" in loaded_setting:
            self.set_salt(b64decode(loaded_setting["salt"]))
        if "length" in loaded_setting:
            self.set_length(loaded_setting["length"])
        if "cDate" in loaded_setting:
            self.set_creation_date(loaded_setting["cDate"])
        if "mDate" in loaded_setting:
            self.set_modification_date(loaded_setting["mDate"])
        if "usedCharacters" in loaded_setting:
            self.set_custom_character_set(loaded_setting["usedCharacters"])
        if "reserved" in loaded_setting:
            self.set_reserved(loaded_setting["reserved"])

    def ask_for_input(self):
        """
        Displays some input prompts for the settings properties.
        """
        self.set_username(input('Benutzername: '))
        wants_legacy_password = input('Möchten Sie ein Passwort generieren (Alternative: nur speichern)? [J/n] ')
        if wants_legacy_password in ['n', 'N', 'speichern', 'save', 'no', 'nein', 'Nein', 'No', 'Nay']:
            self.set_legacy_password(getpass.getpass('klassisches Passwort: '))
        else:
            length_str = input('Passwortlänge [' + str(self.get_length()) + ']: ')
            try:
                length = int(length_str)
                if length <= 0:
                    length = self.get_length()
            except ValueError:
                length = self.get_length()
            self.set_length(length)
            iterations_str = input('Iterationszahl [' + str(self.get_iterations()) + ']: ')
            try:
                iterations = int(iterations_str)
                if iterations <= 0:
                    iterations = self.get_iterations()
            except ValueError:
                iterations = self.get_iterations()
            self.set_iterations(iterations)
