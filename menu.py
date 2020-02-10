# Author: Alejandro Gonzalez Felix
# Email: felix090915@gmail.com
# Github: https://github.com/FELIX090915
from os import system


class Menu:
    def __init__(self, options, label, title='', *, clearScr=False,
                 exitKey='exit', menuFuncArgs=[], caseSensible=False):
        """
        Arguments:
            options {dict} -- A dictionary with the labels as key
                              and references to functions.
            label {string} -- How the menu will be listed in other menus

        Keyword Arguments:
            title {str} -- This is printed at the top of
                           the list of options (default: {''})
            clearScr {bool} -- If true the menu will clear the
                               screen (default: {False})
            exitKey {str} -- What needs to be typed to exit or
                             close the menu (default: {'exit'})
            menuFuncArgs {list} -- Arguments to pass to the next menu
                                   (default: {[]})
            caseSensible {bool} -- If true the user needs to type the options
                                   as they are written (default: {False})
        """

        # Validation of data
        Menu.checkInit(options, label, title='', clearScr=False,
                       exitKey='exit', menuFuncArgs=[], caseSensible=False)

        # Saves the list of functions in the instance object
        self.options = options

        # How to print the menu in case it is inside another menu
        self.label = label
        self.caseSensible = caseSensible

        # Prints at the top of all the options
        self.title = title

        # This is what will be used to exit the menu
        self.exitKey = exitKey
        # Arguments to pass to next menu
        self.menuFuncArgs = menuFuncArgs

        #  For this to work properly the module system from os must be imported
        self.clearScr = clearScr

        # This attributes below this line could be changed accessing
        # directly to them with the dot operator
        self.titleDecorators = '-'

        # This icons are meant to indicate if the option is a menu ir not
        self.subIcon = '+'
        self.actIcon = '-'

        # This
        self.subIndicator = '->'

        # This will be printed between the icon and the name of the option
        self.subSeparator = '|'
        self.actSeparator = '|'

        # Message to be displayed when expecting user input
        self.inputMessage = 'Please type an option and press enter: '
        self.invalidOptionMessage = 'Invalid option, please try again :('

    def __len__(self):
        # Returns the number of options there is in the menu
        return len(self.options)

    def valSelfOptions(self, string):
        for opt in self.options:
            # Check if its other sub menu
            # Returns the object so it can be used as a key later
            if isinstance(opt, Menu):
                # This one IS NOT case sensible
                if not self.caseSensible:
                    if string.casefold() == opt.label.casefold():
                        return (True, opt)
                # This one IS case sensible
                else:
                    if string == opt.label:
                        return (True, opt)
            # Regular string
            # Returns the same string so it doesn't conflict with
            # number of returns
            else:
                # This one IS NOT case sensible
                if not self.caseSensible:
                    if string.casefold() == opt.casefold():
                        return (True, opt)

                # This one IS case sensible
                else:
                    if string == opt:
                        return (True, opt)
        print(string)
        return (False, string)

    def act(self):
        # If its enabled clear the screen
        if self.clearScr:
            try:
                system('cls')
            except NameError:
                print('[WARNING] No module named os')
                print('[WARNING] Unable to clear the screen')
                print('[WARNING] Probably there is an error with \
                      import names or the import is missing')

        # Print title if there is one
        if self.title != '':
            decor = self.titleDecorators * 3
            print(f'{decor} {self.title}')

        # Print all the options
        for opt in self.options:
            if isinstance(opt, Menu):
                print(self.subIcon, opt.label, sep=self.subSeparator)
            else:
                print(self.actIcon, opt, sep=self.actSeparator)
        print('')  # Used to jump one line

        # Get user input
        selected = input(self.inputMessage)

        # Validate user input
        valid, selected = self.valSelfOptions(selected)
        while not valid:
            print(self.invalidOptionMessage)
            selected = input(self.inputMessage)
            valid, selected = self.valSelfOptions(selected)

        # If exit key is entered return false to exit the menu
        if selected == self.exitKey:
            return False
        # If there is another menu
        elif isinstance(selected, Menu):
            # Check if theres a specified function for that menu
            if self.options[selected] is not None:
                try:
                    # Used the specified any function with arguments
                    if self.menuFuncArgs != []:
                        self.options[selected](selected, self.menuFuncArgs)
                        return True
                    else:
                        # Use the specified menu function
                        self.options[selected](selected)
                        return True
                except NameError:
                    print('[ERROR] Could not run the specified menu function')
                    print(f'[ERROR] Either {self.options[selected]} is not a \
                          function or the arguments are wrong')
                    print(f'[ERROR] Arguments: {self.menuFuncArgs}')
                    raise
            else:
                print('Buffering')
                Menu.menuBuffer(selected)
                return True
        # If its not the exit key or other menu then run the
        # function associated with the key
        else:
            self.options[selected]()
            return True

    # ? Maybe there is a better name for this function
    @staticmethod
    def menuBuffer(menu):
        """ Runs continuously a menu until the exit key is typed"""
        running = True
        while running:
            running = menu.act()

    @staticmethod
    def checkInit(options, label, title='', clearScr=False,
                  exitKey='exit', menuFuncArgs=[], caseSensible=False):
        # Check if options is a dictionary
        if not isinstance(options, dict):
            print('[ERROR] Expected dictionary in the \'options\' parameter')
            raise Exception('Parameter \'options\' is not of type \'dict\'')

        # Check if label is string
        if not isinstance(label, str):
            print('[ERROR] Expected a string in the \'label\' parameter')
            raise Exception('Parameter \'label\' is not of type \'string\'')

        # Check if title is string
        if not isinstance(title, str):
            print('[ERROR] Expected a string in the \'title\' parameter')
            raise Exception('Parameter \'title\' is not of type \'string\'')

        # Check if clearScr is boolean
        if not isinstance(clearScr, bool):
            print('[ERROR] Expected a boolean in the \'clearScr\' parameter')
            raise Exception('Parameter \'clearScr\' is \
                             not of type \'boolean\'')

        # Check if caseSensible is boolean
        if not isinstance(caseSensible, bool):
            print('[ERROR] Expected a boolean in the caseSensible parameter')
            raise Exception('Parameter \'caseSensible\' \
                             is not of type \'boolean\'')
        return True
