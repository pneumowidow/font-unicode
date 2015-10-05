#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# font-unicode
# Copyright 2015 Christopher Simpkins
# MIT license
# ------------------------------------------------------------------------------


# Application start
def main():
    import os
    import sys
    from Naked.commandline import Command
    from Naked.toolshed.system import stdout, stderr
    from fontunicode.commands.search import NameSearcher, UnicodeSearcher, UnicodeObject

    # ------------------------------------------------------------------------------------------
    # [ Instantiate command line object ]
    #   used for all subsequent conditional logic in the CLI application
    # ------------------------------------------------------------------------------------------
    c = Command(sys.argv[0], sys.argv[1:])

    # ------------------------------------------------------------------------------------------
    # [ Command Suite Validation ] - early validation of appropriate command syntax
    # Test that user entered at least one argument to the executable, print usage if not
    # ------------------------------------------------------------------------------------------
    if not c.command_suite_validates():
        from fontunicode.settings import usage as fontunicode_usage
        print(fontunicode_usage)
        sys.exit(1)
    # ------------------------------------------------------------------------------------------
    # [ NAKED FRAMEWORK COMMANDS ]
    # Naked framework provides default help, usage, and version commands for all applications
    #   --> settings for user messages are assigned in the lib/fontunicode/settings.py file
    # ------------------------------------------------------------------------------------------
    if c.help():      # User requested fontunicode help information
        from fontunicode.settings import help as fontunicode_help
        print(fontunicode_help)
        sys.exit(0)
    elif c.usage():   # User requested fontunicode usage information
        from fontunicode.settings import usage as fontunicode_usage
        print(fontunicode_usage)
        sys.exit(0)
    elif c.version():  # User requested fontunicode version information
        from fontunicode.settings import app_name, major_version, minor_version, patch_version
        version_display_string = app_name + ' ' + major_version + '.' + minor_version + '.' + patch_version
        print(version_display_string)
        sys.exit(0)

    # ------------------------------------------------------------------------------------------
    # [ PRIMARY COMMAND LOGIC ]
    # ------------------------------------------------------------------------------------------

    if c.cmd == "list":
        adobeglyphlist_text = open(os.path.join(os.path.dirname(__file__), 'glyphlist', 'aglfn.txt')).read()
        print(adobeglyphlist_text)
        sys.exit(0)
    elif c.cmd == "search":
        # if there is not a search, term raise error message and exit
        if c.argc == 1:
            stderr("[font-unicode]: Error: Please enter a Unicode search term.", exit=1)

        search_list = c.argv[1:]  # include all command line arguments after the primary command
        unicode_search_list = []
        name_search_list = []
        # get the data from the Adobe glyph list file and Unicode name list file
        adobeglyphlist_text = open(os.path.join(os.path.dirname(__file__), 'glyphlist', 'aglfn.txt')).read()
        unicodeglyphlist_text = open(os.path.join(os.path.dirname(__file__), 'glyphlist', 'NamesList.txt')).read()

        for needle in search_list:
            if needle.startswith('u+'):
                unicode_search_list.append(needle[2:])  # remove the u+ before adding it to the list for search
            else:
                unicode_search_list.append(needle)

        # instantiate the UnicodeObject from the Adobe list data
        uniobj = UnicodeObject(adobeglyphlist_text, unicodeglyphlist_text)

        if len(unicode_search_list) > 0:
            us = UnicodeSearcher(uniobj)
            for needle in unicode_search_list:
                us.find(needle)

        if len(name_search_list) > 0:
            pass

    elif c.cmd == "name":
        pass


    # ------------------------------------------------------------------------------------------
    # [ DEFAULT MESSAGE FOR MATCH FAILURE ]
    #  Message to provide to the user when all above conditional logic fails to meet a true condition
    # ------------------------------------------------------------------------------------------
    else:
        print("Could not complete the command that you entered.  Please try again.")
        sys.exit(1)  # exit

if __name__ == '__main__':
    main()